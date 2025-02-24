import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig, LlamaForCausalLM
from time import time
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_community.llms import HuggingFacePipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain

from dotenv import load_dotenv
load_dotenv()  # Load environment variables (e.g., API keys)

# -------------------------------------------------------------------------
# Device Selection
# -------------------------------------------------------------------------

# Select the device for computation (GPU if available, otherwise CPU)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using {device} device')

# -------------------------------------------------------------------------
# Model Loading
# -------------------------------------------------------------------------

print('Loading the model...')

# Define the model to use
MODEL_NAME = "GPT"  # Change this value to "LLAMA2" or "FLANT5" as required

if MODEL_NAME == "GPT":
    # ---------------------------------------------------------------------
    # GPT Model Setup
    # ---------------------------------------------------------------------
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema.runnable import RunnablePassthrough
    from langchain.schema.output_parser import StrOutputParser
    import os
    import openai

    # Set your OpenAI API key from the .env file
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Define the GPT model
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

elif MODEL_NAME == "LLAMA2":
    # ---------------------------------------------------------------------
    # LLAMA2 Model Setup
    # ---------------------------------------------------------------------
    model_config = AutoConfig.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
    model = LlamaForCausalLM.from_pretrained(
        "meta-llama/Llama-2-7b-chat-hf",
        trust_remote_code=True, 
        config=model_config, 
        device_map='auto'
    )
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

elif MODEL_NAME == "FLANT5":
    # ---------------------------------------------------------------------
    # Flan-T5 Model Setup
    # ---------------------------------------------------------------------
    model_name = "google/flan-t5-large"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

if MODEL_NAME != "GPT":
    # ---------------------------------------------------------------------
    # Pipeline Creation for Non-GPT Models
    # ---------------------------------------------------------------------
    print('Creating Pipeline...')
    query_pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    llm = HuggingFacePipeline(pipeline=query_pipeline)

# -------------------------------------------------------------------------
# PDF Loading and Splitting
# -------------------------------------------------------------------------

print('Loading the corpus for TESLA...')

# Load the PDF file using LangChain's PyPDFLoader
loader = PyPDFLoader(r"data/tsla-20230930.pdf")
data = loader.load()  # Load the text data from the PDF

# Split the text into manageable chunks
print('Instantiating Text Splitter...')
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=300)
all_splits = text_splitter.split_documents(data)

# -------------------------------------------------------------------------
# Embedding Creation
# -------------------------------------------------------------------------

print('Preparing Embeddings...')

# Define the embedding model to use (HuggingFace's MPNet)
model_name = "sentence-transformers/all-mpnet-base-v2"

# Instantiate the embedding model using LangChain's HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name=model_name)

# -------------------------------------------------------------------------
# Vector Store Preparation
# -------------------------------------------------------------------------

print('Preparing Vector Embeddings...')

# Create a vector store to store the document chunks and their embeddings
# Using LangChain's Chroma as the vector store backend
vectordb = Chroma.from_documents(
    documents=all_splits,  # Provide the split documents
    embedding=embeddings,  # Provide the embedding model
    persist_directory="chroma_db"  # Specify the directory to store the vector database
)

# -------------------------------------------------------------------------
# Chain Preparation
# -------------------------------------------------------------------------

print('Preparing chain...')

if MODEL_NAME == "GPT":
    # ---------------------------------------------------------------------
    # GPT-Specific Chain Setup
    # ---------------------------------------------------------------------

    # Define a prompt template for question-answering
    template = """
    You are an assistant for question-answering tasks for Retrieval Augmented Generation system for the financial reports such as 10Q and 10K.
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Use two sentences maximum and keep the answer concise.
    Question: {question} 
    Context: {context} 
    Answer:
    """
    
    # Create a ChatPromptTemplate using the defined template
    prompt = ChatPromptTemplate.from_template(template)

    # Use the vector database as a retriever
    retriever = vectordb.as_retriever()

    # Define the RAG pipeline using LangChain's pipeline operators
    conversation_chain = (
        {"context": retriever, "question": RunnablePassthrough()} 
        | prompt  # Apply the prompt
        | llm  # Pass the question to the selected GPT model
        | StrOutputParser()  # Parse the output
    )

else:
    # ---------------------------------------------------------------------
    # Non-GPT Chain Setup
    # ---------------------------------------------------------------------

    # Define the chain for models like LLAMA2 or Flan-T5
    conversation_chain = load_qa_chain(llm, chain_type="map_reduce")

print('Chain Prepared...')

from dash.dependencies import Input, Output, State
from app import app

from components.textbox import render_textbox
from pages.chatbot.chatbot_model import conversation_chain, vectordb, MODEL_NAME

@app.callback(
    Output(component_id="display-conversation", component_property="children"),
    Input(component_id="store-conversation", component_property="data")
)
def update_display(chat_history):
    """
    @brief Updates the chat display with the conversation history.

    @details Splits the chat history into individual messages using "<split>" as a delimiter.
             - Renders human messages on the right and AI messages on the left.
             - Alternates between human and AI message bubbles.

    @param chat_history: A string containing the entire conversation history.
    @return: List[html.Div] - A list of Divs, each containing a rendered message bubble.
    """
    return [
        # Render human messages (even indices) and AI messages (odd indices)
        render_textbox(x, box="human") if i % 2 == 0 else render_textbox(x, box="AI")
        for i, x in enumerate(chat_history.split("<split>")[:-1])  # Exclude the last empty split
    ]

@app.callback(
    Output(component_id="user-input", component_property="value"),
    Input(component_id="submit", component_property="n_clicks"),
    Input(component_id="user-input", component_property="n_submit"),
)
def clear_input(n_clicks, n_submit):
    """
    @brief Clears the user input field after submission.

    @details Listens to both the "Send" button click and the "Enter" key submission events.
             - Clears the input field when either event occurs.

    @param n_clicks: Number of clicks on the "Send" button.
    @param n_submit: Number of times the "Enter" key is pressed in the input field.
    @return: str - An empty string to clear the input field.
    """
    return ""

@app.callback(
    Output("store-conversation", "data"),
    Output("loading-component", "children"),
    Input("submit", "n_clicks"),
    Input("user-input", "n_submit"),
    State("user-input", "value"),
    State("store-conversation", "data"),
    State("selected-model", "data"),
)
def run_chatbot(n_clicks, n_submit, user_input, chat_history, selected_model):
    """
    @brief Handles user input and generates chatbot responses.

    @details Executes the following steps:
             1. Checks for user input and handles empty or null values.
             2. Appends the user's input to the conversation history.
             3. Dynamically selects the model to process the response (GPT or other).
             4. Fetches AI-generated output using the selected model.
             5. Appends the chatbot's response to the conversation history.

    @param n_clicks: Number of clicks on the "Send" button.
    @param n_submit: Number of times the "Enter" key is pressed in the input field.
    @param user_input: The text entered by the user.
    @param chat_history: The current conversation history.
    @param selected_model: The model selected by the user (e.g., GPT, LLAMA2).
    @return: Tuple[str, None] - Updated conversation history and `None` for loading component.
    """
    # If no input is provided, do nothing
    if n_clicks == 0 and n_submit is None:
        return "", None

    if not user_input:  # If the input field is empty
        return chat_history, None

    # Initialize conversation history if not already present
    chat_history = chat_history or ""
    # Append the user's input to the conversation history
    chat_history += f"Human: {user_input}<split>ChatBot: "

    try:
        # Handle logic based on the selected model
        if selected_model == "GPT":
            # Use GPT model to generate a response
            output = conversation_chain.invoke(user_input)
        else:
            # Use other models for generating responses
            docs = vectordb.similarity_search(user_input)  # Retrieve similar documents
            inputs = {"input_documents": docs, "question": user_input}
            output = conversation_chain.run(inputs)  # Generate the response
        # Append the chatbot's response to the conversation history
        chat_history += f"{output}<split>"
    except Exception as e:
        # Handle any exceptions in the chatbot logic
        print(f"Error in chatbot logic: {e}")
        return chat_history, None

    return chat_history, None

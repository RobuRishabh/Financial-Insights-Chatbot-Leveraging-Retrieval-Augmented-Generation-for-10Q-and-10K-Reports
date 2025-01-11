import dash_bootstrap_components as dbc
from dash import dcc
from dash import html

# -------------------------------------------------------------------------
# Import Components
# -------------------------------------------------------------------------

from components.navbar import render_navbar  # Navigation bar component
from components.input import render_chat_input  # Chat input component

# -------------------------------------------------------------------------
# Define Chatbot Layout
# -------------------------------------------------------------------------

# Layout to display the conversation history
chatbot_layout = html.Div(
    html.Div(id="display-conversation"),  # Placeholder for conversation updates
    style={
        "overflow-y": "auto",  # Enable vertical scrolling for long conversations
        "display": "flex",  # Flexible layout
        "height": "calc(90vh - 132px)",  # Dynamic height based on viewport
        "flex-direction": "column-reverse",  # Recent messages appear at the bottom
    },
)

# -------------------------------------------------------------------------
# Render Chatbot Layout
# -------------------------------------------------------------------------

def render_chatbot():
    """
    @brief Renders the complete chatbot layout.

    @details This function sets up the chatbot interface with the following components:
             - A navigation bar for branding.
             - A conversation display area.
             - An input field for user queries.
             - A loading spinner to indicate processing.

    @return: html.Div - The chatbot interface layout.
    """
    return html.Div(
        [
            # Render the navigation bar with a brand name
            render_navbar(brand_name="AI Chatbot for Financial Reports (10Q, 10K)"),
            html.Br(),  # Add spacing below the navbar
            
            # Store to hold the conversation data
            dcc.Store(id="store-conversation", data=""),

            # Main container for the chatbot
            dbc.Container(
                fluid=True,  # Use full-width container
                children=[
                    dbc.Row(
                        [
                            # Left spacer column
                            dbc.Col(width=1),

                            # Main content column
                            dbc.Col(
                                width=10,
                                children=dbc.Card(
                                    [
                                        dbc.CardBody([
                                            # Display conversation history
                                            chatbot_layout,

                                            # Chat input field with styling
                                            html.Div(
                                                render_chat_input(),
                                                style={
                                                    'margin-left': '70px',
                                                    'margin-right': '70px',
                                                    'margin-bottom': '20px'
                                                }
                                            ),

                                            # Loading spinner for processing
                                            dbc.Spinner(html.Div(id="loading-component")),
                                        ])
                                    ],
                                    style={
                                        'border-radius': 25,  # Rounded corners for the card
                                        'background': '#FFFFFF',  # White background
                                        'border': '0px solid'  # No border
                                    }
                                )
                            ),

                            # Right spacer column
                            dbc.Col(width=1),
                        ]
                    )
                ]
            ),
        ],
    )

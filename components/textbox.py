from dash import html
import dash_bootstrap_components as dbc
from app import app

def render_textbox(text: str, box: str = "AI"):
    """
    @brief Renders a message bubble for the chat interface.

    @details This function creates a styled message bubble depending on the sender (AI or human).
             - AI messages are aligned to the left with a light theme.
             - Human messages are aligned to the right with a primary theme.
             - Includes thumbnails for AI and human avatars.
             - Supports custom styling for text and layout.

    @param text: The text to display in the message bubble.
    @param box: The type of message box ("AI" or "human"). Default is "AI".
    @return: html.Div - A Div containing the message bubble and the avatar thumbnail.

    @raises ValueError: If the `box` parameter is not "AI" or "human".
    """

    # Remove unwanted prefixes from the text
    text = text.replace(f"ChatBot:", "").replace("Human:", "")

    # Base styling for the message bubble
    style = {
        "max-width": "60%",  # Maximum width for the message bubble
        "width": "max-content",  # Adjust width dynamically based on text length
        "padding": "5px 10px",  # Padding inside the bubble
        "border-radius": 25,  # Rounded corners for the bubble
        "margin-bottom": 20,  # Space below the bubble
        'border': '0px solid'  # No border by default
    }

    if box == "human":
        # Style for human messages (aligned to the right)
        style["margin-left"] = "auto"
        style["margin-right"] = 0

        # Human avatar
        thumbnail_human = html.Img(
            src=app.get_asset_url("human.png"),  # Path to human avatar image
            style={
                "border-radius": 50,  # Circular avatar
                "height": 36,  # Avatar size
                "margin-left": 5,  # Space to the left of the avatar
                "float": "right",  # Align the avatar to the right
            },
        )

        # Human message bubble with a primary color theme
        textbox_human = dbc.Card(text, style=style, body=True, color="primary", inverse=True)

        # Return the avatar and the message bubble
        return html.Div([thumbnail_human, textbox_human])

    elif box == "AI":
        # Style for AI messages (aligned to the left)
        style["margin-left"] = 0
        style["margin-right"] = "auto"

        # AI avatar
        thumbnail = html.Img(
            src=app.get_asset_url("chatbot.png"),  # Path to chatbot avatar image
            style={
                "border-radius": 50,  # Circular avatar
                "height": 36,  # Avatar size
                "margin-right": 5,  # Space to the right of the avatar
                "float": "left",  # Align the avatar to the left
            },
        )

        # AI message bubble with a light color theme
        textbox = dbc.Card(text, style=style, body=True, color="light", inverse=False)

        # Return the avatar and the message bubble
        return html.Div([thumbnail, textbox])

    else:
        # Raise an error if the box type is invalid
        raise ValueError("Incorrect option for `box`.")

import dash_bootstrap_components as dbc

def render_chat_input():
    """
    @brief Renders the chat input field with a send button.

    @details This function creates a user input interface using Dash Bootstrap Components. 
             - The input field allows the user to type messages.
             - The send button triggers the callback to process the user's input.
             - The send button's color can be customized.

    @return dbc.InputGroup: A Dash Bootstrap InputGroup containing the input field and a send button.
    """
    # Define an InputGroup component to group the input field and the send button
    chat_input = dbc.InputGroup(
        children=[
            # Input field for user messages
            dbc.Input(
                id="user-input",  # Unique identifier for the input field
                placeholder="Send a message...",  # Placeholder text
                type="text"  # Input type as text
            ),

            # Send button with a custom color
            dbc.Button(
                id="submit",  # Unique identifier for the button
                children=">",  # Label on the button
                color="primary",  # Change color to "primary" (blue)
                style={"border-radius": "5px"}  # Optional: Add rounded corners to the button
            ),
        ],
    )
    return chat_input  # Return the InputGroup component

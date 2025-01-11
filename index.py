import sys
sys.path.append('path/to/langchain_openai')
from dash.dependencies import Input, Output
from dash import dcc, html 

# import pages
from pages.chatbot.chatbot_view import render_chatbot
from pages.chatbot.chatbot_controller import *
from pages.page_not_found import page_not_found

from app import app


def serve_content():
    """
    @brief Defines the main layout of the application.

    @details Includes:
             - A location tracker to monitor the app's current URL path.
             - A content placeholder to render pages dynamically.
             - A store for the selected model.
    """
    return html.Div([
        dcc.Store(id="selected-model", data="GPT"),  # Store for the selected model
        dcc.Store(id="store-conversation", data=""),  # Store for the conversation
        dcc.Location(id='url', refresh=False),  # Tracks the current URL
        html.Div(id='page-content'),  # Placeholder for dynamic page rendering
    ])

app.layout = serve_content()


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    """
    :param pathname: path of the actual page
    :return: page
    """

    if pathname in '/' or pathname in '/chatbot':
        return render_chatbot()
    return page_not_found()


if __name__ == '__main__':
    app.run_server(debug=True)
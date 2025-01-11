import dash_bootstrap_components as dbc

def render_navbar(brand_name: str = "Chatbot", brand_color: str = "#165AA7"):
    """
    @brief Renders a simple navigation bar for the application.

    @details This function creates a responsive navigation bar using Dash Bootstrap Components (DBC). 
             - Displays the brand name as a clickable link to the home page.
             - The navigation bar color and brand name can be customized.
             - The bar is sticky (remains visible at the top when scrolling).
             - Supports dark mode for better visibility.

    @param brand_name: The name of the application displayed in the navbar (default: "Chatbot").
    @param brand_color: The background color of the navigation bar (default: "#165AA7" - blue).
    @return: dbc.NavbarSimple - A Dash Bootstrap navigation bar component.
    """
    # Create a simple navigation bar with brand name and links
    navbar = dbc.NavbarSimple(
        brand=brand_name,  # Brand name displayed in the navbar
        brand_href="/",  # Link to the homepage when clicking the brand
        color=brand_color,  # Background color of the navbar
        sticky='top',  # Makes the navbar sticky at the top of the page
        links_left=True,  # Aligns any additional links to the left
        dark=True,  # Sets text color to white for better contrast on dark backgrounds
        expand=True  # Makes the navbar responsive (collapsible on smaller screens)
    )
    return navbar

import dash_bootstrap_components as dbc
from dash import html, dcc

# ✅ **Toggle Button (Apple-Style)**
toggle_button = html.Button(
    "☰",
    id="toggle-sidebar",
    n_clicks=0,
    style={
        "position": "fixed",
        "top": "10px",
        "left": "10px",
        "width": "50px",
        "height": "50px",
        "background": "#007bff",
        "color": "white",
        "border": "none",
        "border-radius": "50%",
        "font-size": "20px",
        "cursor": "pointer",
        "box-shadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
        "transition": "0.3s ease-in-out",
    },
)

# ✅ **Collapsible Cricket Menu**
cricket_menu = html.Div(
    [
        html.Button(
            "🏏 Cricket ▼",
            id="cricket-toggle",
            n_clicks=0,
            style={
                "width": "100%",
                "background": "#f0f0f0",
                "border": "none",
                "padding": "10px",
                "text-align": "left",
                "font-size": "16px",
                "cursor": "pointer",
                "border-radius": "5px",
                "transition": "0.3s ease-in-out",
            },
        ),
        html.Div(
            [
                dbc.NavLink("🏆 Women's Premier League", href="/cricket-wpl", active="exact"),
                dbc.NavLink("🌍 Champions Trophy (Coming Soon)", href="#", disabled=True),
                dbc.NavLink("🔥 IPL 2025 (Coming Soon)", href="#", disabled=True),
            ],
            id="cricket-dropdown",
            style={"display": "none", "padding-left": "15px"},
        ),
    ],
)

# ✅ **Sidebar Layout**
sidebar = html.Div(
    [
        html.H2("MelloNex-C", className="display-6", style={"textAlign": "center", "color": "#007bff", "margin-bottom": "20px"}),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink("🏠 Home", href="/", active="exact"),
                cricket_menu,
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "width": "270px",
        "height": "100%",
        "padding": "20px",
        "background-color": "#ffffff",
        "box-shadow": "2px 0px 5px rgba(0, 0, 0, 0.1)",
        "transition": "left 0.3s ease-in-out",
        "overflow-y": "auto",  # Enable scrolling if needed
    },
)

# ✅ **Sidebar Animation Styles**
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": "0px",
    "width": "270px",
    "height": "100%",
    "padding": "20px",
    "background-color": "#ffffff",
    "box-shadow": "2px 0px 5px rgba(0, 0, 0, 0.1)",
    "transition": "left 0.3s ease-in-out",
    "overflow-y": "auto",
}

SIDEBAR_HIDDEN_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": "-270px",  # Moves Sidebar Offscreen
    "width": "270px",
    "height": "100%",
    "padding": "20px",
    "background-color": "#ffffff",
    "box-shadow": "2px 0px 5px rgba(0, 0, 0, 0.1)",
    "transition": "left 0.3s ease-in-out",
    "overflow-y": "auto",
}

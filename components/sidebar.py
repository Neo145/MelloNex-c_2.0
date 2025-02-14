import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# ✅ Sidebar Styles
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "260px",
    "padding": "20px",
    "background-color": "#2c3e50",  # Dark Blue Theme
    "color": "white",
    "transition": "all 0.3s ease-in-out",
    "zIndex": 1000
}

SIDEBAR_HIDDEN_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": "-260px",
    "bottom": 0,
    "width": "260px",
    "padding": "20px",
    "background-color": "#2c3e50",
    "color": "white",
    "transition": "all 0.3s ease-in-out",
    "zIndex": 1000
}

CONTENT_STYLE = {
    "marginLeft": "280px",
    "padding": "20px",
    "transition": "margin-left 0.3s ease-in-out",
}

CONTENT_EXPANDED_STYLE = {
    "marginLeft": "20px",
    "padding": "20px",
    "transition": "margin-left 0.3s ease-in-out",
}

# ✅ Sidebar Layout
sidebar = html.Div(
    [
        html.H2("📊 MelloNex-C", className="text-center"),
        html.Hr(),

        # ✅ Home Link
        dbc.Nav(
            [
                dbc.NavLink("🏠 Home", href="/", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),

        # ✅ Expandable "Cricket" Menu with Toggle
        dbc.Button(
            "🏏 Cricket", id="cricket-toggle", color="primary", className="mb-2", n_clicks=0,
            style={"width": "100%", "textAlign": "left"}
        ),
        html.Div(
            [
                dbc.Nav(
                    [
                        dbc.NavLink("🟢 Women's Premier League", href="/cricket-wpl", active="exact"),
                        dbc.NavLink("🏆 Champions Trophy (Coming Soon)", href="#", disabled=True),
                        dbc.NavLink("🔥 IPL 2025 (Coming Soon)", href="#", disabled=True),
                    ],
                    vertical=True,
                    pills=True,
                )
            ],
            id="cricket-dropdown",
            style={"display": "none", "margin-left": "10px"}
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

# ✅ Sidebar Toggle Button
toggle_button = html.Button(
    "☰", id="toggle-sidebar", n_clicks=0,
    style={"position": "fixed", "top": "15px", "left": "15px", "zIndex": 1100, "fontSize": "20px", "padding": "5px 10px", "background-color": "#3498db", "color": "white", "border": "none", "border-radius": "5px", "cursor": "pointer"}
)

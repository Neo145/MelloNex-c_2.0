from dash import html, dcc

# ✅ Sidebar Styles (Fixed)
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "0",
    "left": "0",
    "height": "100vh",
    "width": "250px",
    "backgroundColor": "#1e1e2f",  # Dark theme
    "color": "#EEEEEE",
    "padding": "20px",
    "transition": "transform 0.3s ease-in-out",
    "transform": "translateX(0)",
    "boxShadow": "4px 0px 10px rgba(0, 0, 0, 0.2)",  # Soft shadow for depth
    "borderRight": "2px solid #007bff"  # Highlighted Edge
}

SIDEBAR_HIDDEN_STYLE = SIDEBAR_STYLE.copy()
SIDEBAR_HIDDEN_STYLE["transform"] = "translateX(-100%)"

# ✅ Sidebar Layout
sidebar = html.Div([
    html.H2("MelloNex-C", style={'textAlign': 'center', 'color': '#00bfff'}),
    html.Hr(),

    # ✅ Home Link
    dcc.Link("🏠 Home", href='/', style={'display': 'block', 'padding': '12px', 'color': '#ffffff', 'fontSize': '16px'}),

    # ✅ Cricket Section (Collapsible)
    html.Button("🏏 Cricket ▼", id="cricket-toggle", n_clicks=0, style={
        'background': 'none', 'border': 'none', 'color': '#ffffff',
        'cursor': 'pointer', 'fontSize': '16px', 'width': '100%',
        'textAlign': 'left', 'padding': '12px'
    }),

    # ✅ Collapsible Links
    html.Div(id="cricket-dropdown", children=[
        dcc.Link('🔹 Women\'s Premier League', href='/cricket-wpl', style={'display': 'block', 'padding': '10px', 'color': '#ffffff'}),
        html.Div('📢 Champions Trophy - Analytics Coming Soon', style={'padding': '10px', 'color': '#ffcc00'}),
        html.Div('📢 IPL - Analytics Coming Soon', style={'padding': '10px', 'color': '#ffcc00'}),
    ], style={'display': 'none'}),  # Hidden by default
], id='sidebar', style=SIDEBAR_STYLE)

# ✅ Toggle Button (Always Visible)
toggle_button = html.Button("☰", id="toggle-sidebar", n_clicks=0, style={
    'position': 'fixed', 'top': '10px', 'left': '10px',
    'fontSize': '24px', 'border': 'none', 'background': 'none',
    'color': '#00bfff',  # Change color to Blue
    'cursor': 'pointer', 'zIndex': '1000'
})

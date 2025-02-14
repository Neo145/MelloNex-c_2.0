import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import os

# ✅ Import Components & Pages
from components.sidebar import sidebar, toggle_button, SIDEBAR_STYLE, SIDEBAR_HIDDEN_STYLE
from pages.wpl import wpl_layout, generate_series_stats, generate_toss_impact, generate_venue_stats

# ✅ File Paths
data_path = r"F:\MelloNex-c 2.0\data\wpl"

# ✅ Load Data with Error Handling
def load_data(filename):
    file_path = os.path.join(data_path, filename)
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"⚠️ WARNING: {filename} not found!")
        return pd.DataFrame()  # Return empty DataFrame if file is missing

# ✅ Load Required Data
match_results = load_data("WPL_Head_to_Head_All.csv")
toss_decision = load_data("WPL_Toss_Analysis.csv")
venue_stats = load_data("WPL_Venue_Analysis_All.csv")

# ✅ Initialize Dash App
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# ✅ Page Content Styles
CONTENT_STYLE = {"marginLeft": "270px", "padding": "20px", "transition": "margin-left 0.3s ease-in-out"}
CONTENT_EXPANDED_STYLE = {"marginLeft": "20px", "padding": "20px", "transition": "margin-left 0.3s ease-in-out"}

# ✅ Define App Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    toggle_button,  # ☰ Toggle Button Always Visible
    sidebar,  # Sidebar Navigation
    html.Div(id='page-content', style=CONTENT_STYLE)
])

# ✅ Sidebar Toggle Callback
@app.callback(
    [Output('sidebar', 'style'), Output('page-content', 'style')],
    [Input('toggle-sidebar', 'n_clicks')],
    [State('sidebar', 'style'), State('page-content', 'style')]
)
def toggle_sidebar(n, sidebar_style, content_style):
    return (SIDEBAR_HIDDEN_STYLE, CONTENT_EXPANDED_STYLE) if n % 2 == 1 else (SIDEBAR_STYLE, CONTENT_STYLE)

# ✅ Cricket Dropdown Toggle Callback
@app.callback(
    Output('cricket-dropdown', 'style'),
    [Input('cricket-toggle', 'n_clicks')],
    [State('cricket-dropdown', 'style')]
)
def toggle_cricket_menu(n, dropdown_style):
    return {'display': 'block'} if n % 2 == 1 else {'display': 'none'}

# ✅ Page Routing Callback
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/cricket-wpl':
        return wpl_layout
    else:
        return html.H3("404 Page Not Found", style={'textAlign': 'center'})

# ✅ Callback for Series Stats Graph
@app.callback(
    Output("series-stats-chart", "figure"),
    [Input("year-dropdown", "value")]
)
def update_series_stats(year):
    return generate_series_stats(year)

# ✅ Callback for Toss Impact Analysis Graph
@app.callback(
    Output("toss-impact-chart", "figure"),
    [Input("year-dropdown", "value")]
)
def update_toss_impact(year):
    return generate_toss_impact(year)

# ✅ Callback for Venue Analysis Graph
@app.callback(
    Output("venue-stats-chart", "figure"),
    [Input("year-dropdown", "value")]
)
def update_venue_stats(year):
    return generate_venue_stats(year)

# ✅ Callback to Show/Hide Series Data Table (Fix: Prevents Crashes)
@app.callback(
    Output("series-stats-table", "children"),
    Output("series-stats-table", "style"),
    [Input("toggle-series-table-btn", "n_clicks")],
    [State("year-dropdown", "value")]
)
def toggle_series_table(n_clicks, year):
    if match_results.empty:
        return html.Div("⚠️ Error: No Data Available"), {"display": "block"}

    df = match_results.copy()

    # Ensure 'season' column exists before filtering
    if "season" in df.columns and year != "overall":
        df = df[df["season"] == int(year)]

    if df.empty:
        return html.Div("⚠️ No matches found for selected season."), {"display": "block"}

    if n_clicks and n_clicks % 2 == 1:
        return dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": col, "id": col} for col in df.columns],
            style_table={'overflowX': 'auto'}
        ), {"display": "block"}
    else:
        return None, {"display": "none"}

# ✅ Callback to Show/Hide Toss Impact Data Table
@app.callback(
    Output("toss-stats-table", "children"),
    Output("toss-stats-table", "style"),
    [Input("toggle-toss-table-btn", "n_clicks")],
    [State("year-dropdown", "value")]
)
def toggle_toss_table(n_clicks, year):
    if toss_decision.empty:
        return html.Div("⚠️ Error: No Data Available"), {"display": "block"}

    df = toss_decision.copy()

    if "season" in df.columns and year != "overall":
        df = df[df["season"] == int(year)]

    if df.empty:
        return html.Div("⚠️ No toss data for selected season."), {"display": "block"}

    if n_clicks % 2 == 1:
        return dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": col, "id": col} for col in df.columns],
            style_table={'overflowX': 'auto'}
        ), {"display": "block"}
    else:
        return None, {"display": "none"}

# ✅ Callback to Show/Hide Venue Stats Data Table
@app.callback(
    Output("venue-stats-table", "children"),
    Output("venue-stats-table", "style"),
    [Input("toggle-venue-table-btn", "n_clicks")],
    [State("year-dropdown", "value")]
)
def toggle_venue_table(n_clicks, year):
    if venue_stats.empty:
        return html.Div("⚠️ Error: No Data Available"), {"display": "block"}

    df = venue_stats.copy()

    if "season" in df.columns and year != "overall":
        df = df[df["season"] == int(year)]

    if df.empty:
        return html.Div("⚠️ No venue data for selected season."), {"display": "block"}

    if n_clicks % 2 == 1:
        return dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": col, "id": col} for col in df.columns],
            style_table={'overflowX': 'auto'}
        ), {"display": "block"}
    else:
        return None, {"display": "none"}

# ✅ Run the App
if __name__ == '__main__':
    app.run_server(debug=True)

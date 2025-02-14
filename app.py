import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import os
from flask import Flask  # Required for Gunicorn

# ✅ Import Graph Generation Functions
from pages.wpl import generate_series_stats, generate_toss_impact, generate_venue_stats

# ✅ Flask Server for Gunicorn
server = Flask(__name__)  # Gunicorn needs this

# ✅ Initialize Dash App
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)

# ✅ File Paths (for Data Loading)
data_path = os.getenv("DATA_PATH", "data/wpl")  # Use env variable for flexible deployment

# ✅ Load Data with Error Handling
def load_data(filename):
    file_path = os.path.join(data_path, filename)
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"⚠️ WARNING: {filename} not found!")
        return pd.DataFrame()

# ✅ Load Required Data
match_results = load_data("WPL_Head_to_Head_All.csv")
toss_decision = load_data("WPL_Toss_Analysis.csv")
venue_stats = load_data("WPL_Venue_Analysis_All.csv")

# ✅ Define App Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Handles URL changes

    html.Button("☰ Toggle Sidebar", id="toggle-sidebar", n_clicks=0),
    html.Div(id='sidebar', style={"display": "block"}),

    html.Div(id='page-content', style={"marginLeft": "250px", "padding": "20px"})
])

# ✅ Sidebar Toggle Callback
@app.callback(
    Output('sidebar', 'style'),
    Output('page-content', 'style'),
    [Input('toggle-sidebar', 'n_clicks')],
    [State('sidebar', 'style'), State('page-content', 'style')]
)
def toggle_sidebar(n, sidebar_style, content_style):
    return ({"display": "none"}, {"marginLeft": "20px"}) if n % 2 == 1 else ({"display": "block"}, {"marginLeft": "250px"})

# ✅ Page Routing Callback (Fix: Set Default Page to /cricket-wpl)
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname in ['/', '/cricket-wpl']:  # 🛠 Fix: Load cricket-wpl by default
        return html.Div([
            html.H1("🏏 WPL 2023-2024 Analysis"),
            dcc.Dropdown(
                id="year-dropdown",
                options=[
                    {'label': 'WPL 2023', 'value': '2023'},
                    {'label': 'WPL 2024', 'value': '2024'},
                    {'label': 'All Matches', 'value': 'overall'}
                ],
                value="overall",
                clearable=False,
                style={'width': '50%'}
            ),
            dcc.Graph(id="series-stats-chart"),
            html.Button("🔍 Toggle Series Data", id="toggle-series-table-btn", n_clicks=0),
            html.Div(id="series-stats-table", style={"display": "none"}),

            dcc.Graph(id="toss-impact-chart"),
            html.Button("🔍 Toggle Toss Data", id="toggle-toss-table-btn", n_clicks=0),
            html.Div(id="toss-stats-table", style={"display": "none"}),

            dcc.Graph(id="venue-stats-chart"),
            html.Button("🔍 Toggle Venue Data", id="toggle-venue-table-btn", n_clicks=0),
            html.Div(id="venue-stats-table", style={"display": "none"})
        ])
    return html.H3("404 Page Not Found", style={'textAlign': 'center'})

# ✅ Update Graphs Based on Year Selection
@app.callback(
    [Output("series-stats-chart", "figure"),
     Output("toss-impact-chart", "figure"),
     Output("venue-stats-chart", "figure")],
    [Input("year-dropdown", "value")]
)
def update_graphs(year):
    return generate_series_stats(year), generate_toss_impact(year), generate_venue_stats(year)

# ✅ Show/Hide Data Tables for Analysis
@app.callback(
    [Output("series-stats-table", "children"),
     Output("series-stats-table", "style"),
     Output("toss-stats-table", "children"),
     Output("toss-stats-table", "style"),
     Output("venue-stats-table", "children"),
     Output("venue-stats-table", "style")],
    [Input("toggle-series-table-btn", "n_clicks"),
     Input("toggle-toss-table-btn", "n_clicks"),
     Input("toggle-venue-table-btn", "n_clicks")],
    [State("year-dropdown", "value")]
)
def toggle_tables(series_clicks, toss_clicks, venue_clicks, year):
    def get_table(df, clicks):
        if df.empty:
            return html.Div("⚠️ No Data Available"), {"display": "block"}
        
        if "season" in df.columns and year != "overall":
            df = df[df["season"] == int(year)]

        if clicks % 2 == 1:
            return dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{"name": col, "id": col} for col in df.columns],
                style_table={'overflowX': 'auto'}
            ), {"display": "block"}
        return None, {"display": "none"}

    return (
        get_table(match_results, series_clicks),
        get_table(toss_decision, toss_clicks),
        get_table(venue_stats, venue_clicks)
    )

# ✅ Run the App (Fix Port Binding)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Ensure Render assigns the correct port
    app.run_server(debug=False, host="0.0.0.0", port=port)

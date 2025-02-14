import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import os
import plotly.express as px

# ✅ File Paths
data_path = os.getenv("DATA_PATH", "data/wpl")  # Allows flexibility for deployment

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

# ✅ Dropdown for Year Selection
year_dropdown = dcc.Dropdown(
    id="year-dropdown",
    options=[
        {'label': 'WPL 2023', 'value': '2023'},
        {'label': 'WPL 2024', 'value': '2024'},
        {'label': 'All Matches', 'value': 'overall'}
    ],
    value="overall",
    clearable=False,
    style={'width': '50%'}
)

# ✅ Layout for WPL Page
wpl_layout = html.Div([
    html.H2("🏏 WPL 2023-2024 Analysis", style={'textAlign': 'center'}),

    html.Label("Select Season:"),
    year_dropdown,

    dcc.Tabs(id="wpl-tabs", value='series-stats', children=[
        dcc.Tab(label='📊 Series Statistics', value='series-stats'),
        dcc.Tab(label='🎭 Toss Impact Analysis', value='toss-impact'),
        dcc.Tab(label='📍 Venue Statistics', value='venue-stats'),
        dcc.Tab(label='⚔️ Head-to-Head Analysis', value='h2h-analysis')
    ]),

    html.Div(id="wpl-tab-content")
])

# ✅ Callback to update graphs dynamically based on year selection
@dash.callback(
    Output("wpl-tab-content", "children"),
    [Input("wpl-tabs", "value"), Input("year-dropdown", "value")]
)
def update_graphs(selected_tab, year):
    if selected_tab == "series-stats":
        return dcc.Graph(id="series-stats-chart", figure=generate_series_stats(year))
    elif selected_tab == "toss-impact":
        return dcc.Graph(id="toss-impact-chart", figure=generate_toss_impact(year))
    elif selected_tab == "venue-stats":
        return dcc.Graph(id="venue-stats-chart", figure=generate_venue_stats(year))
    elif selected_tab == "h2h-analysis":
        return generate_head_to_head_table(year)
    return html.H3("⚠️ Error: Tab Not Found")

# ✅ Generate Series Statistics Graph (Fix: Ensures Proper Dynamic Update)
def generate_series_stats(year):
    df = match_results.copy()
    
    if df.empty:
        return px.bar(title="⚠️ No Data Available")

    df["Matchup"] = df["level_0"] + " vs " + df["level_1"]

    # ✅ Filter for selected season
    if "season" in df.columns and year != "overall":
        df = df[df["season"] == int(year)]
    
    fig = px.bar(
        df.sort_values(by="Total Matches", ascending=False),
        x="Total Matches", y="Matchup",
        title=f"Total Matches Played Between Teams ({year})",
        labels={"Matchup": "Team vs Team", "Total Matches": "Number of Matches"},
        color="Total Matches",
        orientation="h"
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=600)
    fig.update_traces(text=df["Total Matches"], textposition='inside')

    return fig

# ✅ Generate Toss Impact Graph (Fix: Ensures Proper Filtering)
def generate_toss_impact(year):
    df = toss_decision.copy()

    if df.empty:
        return px.pie(title="⚠️ No Data Available")

    if "season" in df.columns and year != "overall":
        df = df[df["season"] == int(year)]

    fig = px.pie(
        df, names="Team", values="Toss Success Rate (%)",
        title=f"Toss Success Rate by Team ({year})",
        labels={"Team": "Teams", "Toss Success Rate (%)": "Win Percentage"},
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_traces(textinfo='percent+label')

    return fig

# ✅ Generate Venue Statistics Graph (Fix: Ensures Sorting and Labels)
def generate_venue_stats(year):
    df = venue_stats.copy()

    if df.empty:
        return px.bar(title="⚠️ No Data Available")

    if "season" in df.columns and year != "overall":
        df = df[df["season"] == int(year)]

    fig = px.bar(
        df.sort_values(by="Total Matches", ascending=False),
        x="venue", y=["Batting First Wins", "Batting Second Wins"],
        title=f"Matches Won by Batting First vs Batting Second ({year})",
        labels={"venue": "Venue", "value": "Number of Wins"},
        barmode="group",
        color_discrete_map={"Batting First Wins": "blue", "Batting Second Wins": "red"}
    )
    fig.update_layout(xaxis_tickangle=-45)

    return fig

# ✅ Generate Head-to-Head Analysis Table
def generate_head_to_head_table(year):
    df = match_results.copy()

    if df.empty:
        return html.Div("⚠️ No Data Available")

    # ✅ Filter by selected year
    if "season" in df.columns and year != "overall":
        df = df[df["season"] == int(year)]

    # ✅ Data Table
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": col, "id": col} for col in df.columns],
        style_table={'overflowX': 'auto'}
    )


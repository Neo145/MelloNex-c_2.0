# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import pickle
# import json
# from io import StringIO

# # 🎨 **Page Configuration & Styling**
# st.set_page_config(page_title="MelloNex-c: WPL Dashboard", layout="wide")

# st.markdown(
#     """
#     <style>
#         body { background-color: #f5f7fa; }
#         .title { text-align: center; color: #ff4b4b; font-size: 36px; font-weight: bold; }
#         .subheader { text-align: center; font-size: 18px; color: #555; }
#         .card { background: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 10px; }
#         .win { background-color: #5cb85c; color: white; padding: 4px 8px; border-radius: 5px; font-weight: bold; }
#         .loss { background-color: #d9534f; color: white; padding: 4px 8px; border-radius: 5px; font-weight: bold; }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # ✅ **Load Data**
# data_file = "F:/MelloNex-c 2.0/data/processed/Wpl_Processed_Stats_Advanced.csv"
# try:
#     df = pd.read_csv(data_file)
#     st.success("✅ Data Loaded Successfully!")
# except FileNotFoundError:
#     st.error(f"Error: Data file not found at {data_file}")
#     st.stop()

# # ✅ **Fix Chained Assignment Issue Using .loc**
# df.loc[:, "winner_runs"].fillna(0, inplace=True)
# df.loc[:, "winner_wickets"].fillna(0, inplace=True)

# # ✅ **Handle Missing Venue Data Gracefully**
# if "venue" not in df.columns:
#     df["venue"] = "Unknown"

# # ✅ **Team Selection Sidebar**
# st.sidebar.header("🔍 Compare Teams & Predict Winner")
# team1 = st.sidebar.selectbox("Select Team 1", df["team1"].unique())
# team2 = st.sidebar.selectbox("Select Team 2", df["team2"].unique())

# # 🎯 **Head-to-Head Statistics**
# st.markdown("<h2 class='title'>📊 Head-to-Head Stats</h2>", unsafe_allow_html=True)

# stats = df[(df["team1"] == team1) & (df["team2"] == team2)]

# if stats.empty:
#     st.warning(f"No match data found between {team1} and {team2}.")
# else:
#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("📊 Total Matches", stats["total matches"].values[0])
#     col2.metric("🏆 Wins", stats["wins"].values[0])
#     col3.metric("❌ Losses", stats["losses"].values[0])
#     col4.metric("🤝 Tied Matches", stats["tied matches"].values[0])

#     # 🎯 **Last 5 Matches Head-to-Head**
#     st.markdown("<h2 class='title'>📅 Last 5 Matches Head-to-Head</h2>", unsafe_allow_html=True)

#     last_5_matches = stats["last 5 matches"].values[0]
#     if isinstance(last_5_matches, str):
#         last_5_matches = json.loads(last_5_matches)

#     if last_5_matches:
#         last_5_df = pd.DataFrame(last_5_matches)

#         for _, row in last_5_df.iterrows():
#             winner = row["winner"]
#             margin = (
#                 f"🏆 {winner} Won by {int(row['winner_runs'])} runs"
#                 if row["winner_runs"] > 0 else
#                 f"🏆 {winner} Won by {int(row['winner_wickets'])} wickets"
#             )

#             st.markdown(f"""
#                 <div class='card'>
#                     <b>{row["team1"]} vs {row["team2"]}</b> <br>
#                     <span class='win'>{margin}</span>
#                 </div>
#             """, unsafe_allow_html=True)
#     else:
#         st.warning("⚠️ No last 5 matches data available.")

#     # 🎯 **Batting First vs Batting Second Wins Analysis**
#     st.markdown("<h2 class='title'>🏏 Batting First vs Batting Second Wins</h2>", unsafe_allow_html=True)

#     batting_first_wins = stats[stats["toss_decision"] == "bat"]["winner"].value_counts().get(team1, 0)
#     batting_second_wins = stats[stats["toss_decision"] == "bowl"]["winner"].value_counts().get(team1, 0)

#     bat_chart = px.pie(
#         names=["Batting First Wins", "Batting Second Wins"],
#         values=[batting_first_wins, batting_second_wins],
#         title="Batting First vs Second Wins"
#     )
#     st.plotly_chart(bat_chart)

#     # 🎯 **Win Margin Analysis**
#     st.markdown("<h2 class='title'>📊 Win Margin Insights</h2>", unsafe_allow_html=True)
#     win_df = stats[(stats["win by runs"] > 0) | (stats["win by wickets"] > 0)]
    
#     if not win_df.empty:
#         win_df["win_margin"] = win_df["win by runs"].fillna(0) + win_df["win by wickets"].fillna(0) * -1
#         win_chart = px.bar(win_df, x="total matches", y="win_margin", color="winner", title="Win Margins Over Time")
#         st.plotly_chart(win_chart)
#     else:
#         st.warning("⚠️ No win margin data found for analysis!")

#     # 🎯 **Venue Performance Heatmap**
#     st.markdown("<h2 class='title'>🏟️ Venue Performance</h2>", unsafe_allow_html=True)
#     venue_chart = px.bar(df.groupby("venue")["wins"].sum().reset_index(), x="venue", y="wins", title="Venue Performance Heatmap", color="wins")
#     st.plotly_chart(venue_chart)

# # 🎯 **AI Prediction**
# st.sidebar.header("🧠 AI Match Winner Prediction")
# toss_winner = st.sidebar.selectbox("Select Toss Winner", [team1, team2])
# toss_decision = st.sidebar.radio("Toss Decision", ["bat", "bowl"])

# if st.sidebar.button("🔮 Predict Winner"):
#     model_file = "F:/MelloNex-c 2.0/src/api/models/wpl_winner_prediction.pkl"
#     try:
#         with open(model_file, "rb") as f:
#             model, label_encoders = pickle.load(f)

#         input_data = pd.DataFrame([[label_encoders["team1"].transform([team1])[0],
#                                      label_encoders["team2"].transform([team2])[0],
#                                      label_encoders["toss_winner"].transform([toss_winner])[0],
#                                      label_encoders["toss_decision"].transform([toss_decision])[0]]],
#                                   columns=["team1", "team2", "toss_winner", "toss_decision"])

#         prediction = model.predict(input_data)[0]
#         predicted_winner = team1 if prediction == 1 else team2
#         st.sidebar.success(f"🏆 AI Predicts: **{predicted_winner}** will win!")

#     except Exception as e:
#         st.sidebar.error(f"Error during prediction: {e}")

# # 🔥 **End of Page Credit**
# st.markdown("<p style='text-align: center; color: grey;'>🚀 Built with ❤️ by Neo Skye</p>", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

# 1. Data Directory (Set your correct path)
DATA_FOLDER = "F:\\MelloNex-c 2.0\\data\\intermediate"

# 2. Load CSV Function

def load_csv(filename):
    file_path = os.path.join(DATA_FOLDER, filename)
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error(f"Error: File not found at {file_path}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error reading {filename}: {e}")
        return pd.DataFrame()

# 3. Streamlit App
st.title("MelloNex - C WPL Match Analysis Dashboard")

st.write("This dashboard provides interactive visualizations and analysis of Women's Premier League (WPL) match data. Explore toss decisions, venue performance, and head-to-head records for different teams and seasons.")

# Sidebar for selections
st.sidebar.title("Selections")
analysis_type = st.sidebar.selectbox("Select Analysis Type", ['Toss Decision Analysis', 'Venue Performance', 'Last 5 Head-to-Head Matches'])
season = st.sidebar.selectbox("Select Season", ['2023', '2024', 'Overall'])

# Team Selection (only for H2H)
if analysis_type == 'Last 5 Head-to-Head Matches':
    venue_df = load_csv("processed_venue_stats_overall.csv")
    available_teams = sorted(set(venue_df['venue'].dropna())) if not venue_df.empty and 'venue' in venue_df.columns else []
    team1 = st.sidebar.selectbox("Select Team 1", available_teams)
    team2 = st.sidebar.selectbox("Select Team 2", available_teams)
else:
    team1, team2 = None, None

# Load Data
filename = None
if analysis_type == 'Toss Decision Analysis':
    filename = f"processed_toss_decision_{season}.csv"
elif analysis_type == 'Venue Performance':
    filename = f"processed_venue_stats_{season}.csv"
elif analysis_type == 'Last 5 Head-to-Head Matches' and team1 and team2:
    filename = f"last_5_h2h_{team1}_vs_{team2}.csv"

if filename:
    df = load_csv(filename)
    if not df.empty:
        st.write("### Data Table")
        st.dataframe(df)

        # Visualization
        if analysis_type == 'Toss Decision Analysis' and 'toss_decision' in df.columns and 'winner' in df.columns:
            toss_wins = df.groupby('toss_decision')['winner'].count().reset_index()
            fig = go.Figure(data=[go.Pie(labels=toss_wins['toss_decision'], values=toss_wins['winner'], hoverinfo='percent', textinfo='label+percent')])
            fig.update_layout(title="Toss Decision Impact on Wins")
            st.plotly_chart(fig)

        elif analysis_type == 'Venue Performance' and 'venue' in df.columns and 'winner' in df.columns:
            venue_stats = df.groupby('venue')['winner'].count().reset_index()
            fig = go.Figure(data=[go.Bar(x=venue_stats['venue'], y=venue_stats['winner'])])
            fig.update_layout(title="Win Count by Venue", xaxis_title="Venue", yaxis_title="Win Count")
            st.plotly_chart(fig)

        elif analysis_type == 'Last 5 Head-to-Head Matches' and 'winner' in df.columns:
            team_wins = df['winner'].value_counts().reset_index()
            fig = go.Figure(data=[go.Bar(x=team_wins['index'], y=team_wins['winner'])])
            fig.update_layout(title=f"Head-to-Head: {team1} vs {team2}", xaxis_title="Team", yaxis_title="Wins")
            st.plotly_chart(fig)
    else:
        st.warning("No data available for the selected criteria.")
else:
    st.warning("Please select valid inputs.")

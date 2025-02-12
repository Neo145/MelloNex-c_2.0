import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import json
from io import StringIO

# ✅ Page Configuration
st.set_page_config(page_title="MelloNex-c: WPL Dashboard", layout="wide")

# ✅ Data Loading
data_file = r"F:\MelloNex-c 2.0\data\processed\Wpl_Processed_Stats_Advanced.csv"  # Replace with your actual path
try:
    df = pd.read_csv(data_file)
    st.success("✅ Data Loaded Successfully!")
except FileNotFoundError:
    st.error(f"Error: Data file not found at {data_file}")
    st.stop()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# ✅ Missing Column Handling
expected_columns = [
    "team1", "team2", "total matches", "wins", "losses", "tied matches",
    "toss_wins", "toss_decision", "win by runs", "win by wickets", "venue",
    "last 5 matches", "team1 recent form", "team2 recent form"
]

missing_cols = []
for col in expected_columns:
    if col not in df.columns:
        missing_cols.append(col)
        if col not in ["team1", "team2", "last 5 matches", "venue"]:
            df[col] = 0
        else:
            df[col] = "Unknown"

if missing_cols:
    st.warning(f"⚠️ Missing columns: {', '.join(missing_cols)}. Default values used.")

# ✅ JSON Parsing
def parse_last_5_matches(json_data):
    if isinstance(json_data, str):
        try:
            return pd.read_json(StringIO(json_data))
        except json.JSONDecodeError:
            st.warning(f"Invalid JSON for 'last 5 matches': {json_data[:100]}...")
            return pd.DataFrame()
    elif isinstance(json_data, pd.DataFrame):
        return json_data
    else:
        return pd.DataFrame()

df["last 5 matches"] = df["last 5 matches"].apply(parse_last_5_matches)

# ✅ Model Loading
model_file = r"F:\MelloNex-c 2.0\src\api\models\wpl_winner_prediction.pkl"  # Replace with your actual path
try:
    with open(model_file, "rb") as f:
        model, label_encoders = pickle.load(f)
except FileNotFoundError:
    st.error(f"Error: Model file not found at {model_file}")
    st.stop()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()


# 🎨 UI
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🏏 MelloNex-c: WPL Analytics Dashboard</h1>", unsafe_allow_html=True)

# 🎯 Team Selection
st.sidebar.header("🔍 Compare Teams & Predict Winner")
team1 = st.sidebar.selectbox("Select Team 1", df["team1"].unique())
team2 = st.sidebar.selectbox("Select Team 2", df["team2"].unique())

# ✅ Match Statistics
st.subheader(f"📊 **{team1} vs {team2} - Head-to-Head Stats**")

stats = df[(df["team1"] == team1) & (df["team2"] == team2)]

if stats.empty:
    st.warning(f"No match data found between {team1} and {team2}.")
else:
    col1, col2, col3, col4 = st.columns(4)

    total_matches = stats["total matches"].values[0] if "total matches" in stats else 0
    wins = stats["wins"].values[0] if "wins" in stats else 0
    losses = stats["losses"].values[0] if "losses" in stats else 0
    tied_matches = stats["tied matches"].values[0] if "tied matches" in stats else 0

    col1.metric("📊 Total Matches", total_matches)
    col2.metric("🏆 Wins", wins)
    col3.metric("❌ Losses", losses)
    col4.metric("🤝 Tied Matches", tied_matches)

    # ✅ Recent Form
    st.subheader("🔄 Recent Form")
    form1 = stats["team1 recent form"].values[0] if "team1 recent form" in stats else "N/A"
    form2 = stats["team2 recent form"].values[0] if "team2 recent form" in stats else "N/A"
    st.write(f"**{team1} Recent Form:** {form1}  |  **{team2} Recent Form:** {form2}")

    # ✅ Venue Performance
    st.subheader("🏟️ Stadium Performance")
    if "venue" in df.columns and len(df["venue"].unique()) > 1:
        venue_chart = px.bar(df.groupby("venue")["wins"].sum().reset_index(), x="venue", y="wins", title="Stadium Performance", color="wins")
        st.plotly_chart(venue_chart)
    elif "venue" not in df.columns:
        st.info("Venue data is missing. Cannot display stadium performance chart.")
    else:
        st.info("Only one venue found. Stadium performance chart not displayed.")

    # ✅ Toss Decision Analysis
    toss_chart = px.pie(names=["Chose to Bat", "Chose to Bowl"], 
                        values=[stats["toss_decision"].value_counts().get("bat", 0), 
                                stats["toss_decision"].value_counts().get("bowl", 0)], 
                        title="🌀 Toss Decision Trends")
    st.plotly_chart(toss_chart)

    # ✅ Win Margin Analysis
    st.subheader("📊 Win Margin Analysis (Every Match)")

    win_df = df[ (df["win by runs"] > 0) | (df["win by wickets"] > 0)]
    if not win_df.empty:
        try:
            if "date" in win_df.columns:
                win_df["date"] = pd.to_datetime(win_df["date"])
                x_axis = win_df["date"]
                title = "Win Margin Over Time"
            else:
                x_axis = win_df.index
                title = "Win Margin (Match Number)"
                st.warning("⚠️ No 'date' column found. Displaying win margin by match number.")

            win_df["win_margin"] = win_df["win by runs"].fillna(0) + win_df["win by wickets"].fillna(0) * -1

            win_chart = px.bar(win_df, x=x_axis, y="win_margin", color="winner", title=title,
                            text="win_margin", hover_data=["win by runs", "win by wickets"])
            st.plotly_chart(win_chart)
        except Exception as e:
            st.error(f"Error creating Win Margin chart: {e}")
    else:
        st.warning("⚠️ No win margin data (runs or wickets) found for analysis!")

    # ✅ Last 5 Matches Head-to-Head
    st.subheader("📅 Last 5 Matches Head-to-Head")
    last_5_matches = stats["last 5 matches"].values[0] if "last 5 matches" in stats else pd.DataFrame()
    if not last_5_matches.empty:
        st.table(last_5_matches)
    else:
        st.warning("⚠️ No last 5 matches data available.")

# ✅ AI Prediction
st.sidebar.header("🧠 AI Match Winner Prediction")
toss_winner = st.sidebar.selectbox("Select Toss Winner", [team1, team2])
toss_decision = st.sidebar.radio("Toss Decision", ["bat", "bowl"])

if st.sidebar.button("🔮 Predict Winner"):
    try:
        input_data = pd.DataFrame([[label_encoders["team1"].transform([team1])[0],
                                 label_encoders["team2"].transform([team2])[0],
                                 label_encoders["toss_winner"].transform([toss_winner])[0],
                                 label_encoders["toss_decision"].transform([toss_decision])[0], 1, 1]],
                                columns=["team1", "team2", "toss_winner", "toss_decision", "matches", "toss_wins"])
        prediction = model.predict(input_data)[0]
        predicted_winner = team1 if prediction == 1 else team2
        st.sidebar.success(f"🏆 AI Predicts: **{predicted_winner}** will win!")
    except Exception as e:
        st.error(f"Error during prediction: {e}")
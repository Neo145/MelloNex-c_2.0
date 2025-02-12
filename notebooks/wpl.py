import pandas as pd
import os

# ✅ Define file paths
input_file = r"F:\MelloNex-c 2.0\data\raw\Wpl 2023-2024.csv"
output_file = r"F:\MelloNex-c 2.0\data\processed\Wpl_Processed_Stats_Advanced.csv"

# ✅ Load dataset
df = pd.read_csv(input_file)

# ✅ Convert match dates to proper datetime format
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year

# ✅ Ensure column names are clean
df.columns = df.columns.str.strip().str.lower()

# ✅ Rename columns for consistency
df.rename(columns={"team": "team1", "opponent": "team2"}, inplace=True)

# ✅ Ensure Venue Column Exists
if "venue" not in df.columns:
    df["venue"] = "Unknown Venue"

# ✅ Function to compute team vs team statistics
def compute_team_vs_team_stats(df):
    summary = []
    teams = df["team1"].unique()

    for team1 in teams:
        for team2 in teams:
            if team1 == team2:
                continue  # Skip self-comparison

            # ✅ Filter matches between the two teams
            matches = df[((df['team1'] == team1) & (df['team2'] == team2)) |
                         ((df['team1'] == team2) & (df['team2'] == team1))]

            total_matches = len(matches)
            team1_wins = (matches['winner'] == team1).sum()
            team2_wins = (matches['winner'] == team2).sum()
            no_result = matches['winner'].isna().sum()
            tied_matches = ((matches['winner'] == "Tie") | (matches['winner'] == "Draw")).sum()

            # ✅ Toss Impact
            toss_wins = (matches['toss_winner'] == team1).sum()
            toss_won_match_won = ((matches['toss_winner'] == team1) & (matches['winner'] == team1)).sum()
            toss_won_match_lost = ((matches['toss_winner'] == team1) & (matches['winner'] == team2)).sum()
            toss_lost_match_won = ((matches['toss_winner'] == team2) & (matches['winner'] == team1)).sum()
            toss_lost_match_lost = ((matches['toss_winner'] == team2) & (matches['winner'] == team2)).sum()

            # ✅ Toss Decision Analysis
            chose_to_bat = ((matches['toss_winner'] == team1) & (matches['toss_decision'] == "bat")).sum()
            chose_to_bowl = ((matches['toss_winner'] == team1) & (matches['toss_decision'] == "bowl")).sum()

            # ✅ Batting First vs Second Wins
            batting_first_wins = ((matches['toss_decision'] == "bat") & (matches['winner'] == team1)).sum()
            batting_second_wins = ((matches['toss_decision'] == "bowl") & (matches['winner'] == team1)).sum()

            # ✅ Win Margins (Runs & Wickets)
            win_by_runs = matches.loc[matches['winner'] == team1, 'winner_runs'].sum()
            win_by_wickets = matches.loc[matches['winner'] == team1, 'winner_wickets'].sum()

            # ✅ Last 5 Matches (Sorted by Most Recent)
            last_5_matches = matches[['date', 'team1', 'team2', 'winner', 'winner_runs', 'winner_wickets']].sort_values(by='date', ascending=False).head(5)
            last_5_matches['date'] = last_5_matches['date'].dt.strftime('%Y-%m-%d')
            last_5_matches_str = last_5_matches.to_json(orient="records")

            # ✅ Compute Recent Form (Last 5 Match Results)
            def get_recent_form(matches, team):
                last_5 = matches.sort_values(by="date", ascending=False).head(5)
                results = []
                for _, match in last_5.iterrows():
                    if pd.isna(match["winner"]):
                        results.append("NR")  # No Result
                    elif match["winner"] == team:
                        results.append("W")  # Win
                    else:
                        results.append("L")  # Loss
                return "".join(results)

            team1_recent_form = get_recent_form(matches, team1)
            team2_recent_form = get_recent_form(matches, team2)

            # ✅ Append results
            summary.append({
                "team1": team1,
                "team2": team2,
                "total matches": total_matches,
                "wins": team1_wins,
                "losses": team2_wins,
                "no result": no_result,
                "tied matches": tied_matches,
                "toss_wins": toss_wins,
                "toss_winner": team1 if toss_wins > 0 else team2,  # ✅ Add toss winner
                "winner": team1 if team1_wins > team2_wins else team2,  # ✅ Add match winner
                "toss won & match won": toss_won_match_won,
                "toss won & match lost": toss_won_match_lost,
                "toss lost & match won": toss_lost_match_won,
                "toss lost & match lost": toss_lost_match_lost,
                "toss_decision": "bat" if chose_to_bat > chose_to_bowl else "bowl",  # ✅ Add toss decision
                "chose to bat": chose_to_bat,
                "chose to bowl": chose_to_bowl,
                "batting first wins": batting_first_wins,
                "batting second wins": batting_second_wins,
                "win by runs": win_by_runs,  # ✅ Add win by runs
                "win by wickets": win_by_wickets,  # ✅ Add win by wickets
                "winner_runs": matches[matches["winner"] == team1]["winner_runs"].sum(),  # ✅ Fix winner runs
                "winner_wickets": matches[matches["winner"] == team1]["winner_wickets"].sum(),  # ✅ Fix winner wickets
                "last 5 matches": last_5_matches_str,
                "team1 recent form": team1_recent_form,  # ✅ New Feature
                "team2 recent form": team2_recent_form   # ✅ New Feature
            })

    return pd.DataFrame(summary)

# ✅ Process the data
processed_df = compute_team_vs_team_stats(df)

# ✅ Save the processed data
os.makedirs(os.path.dirname(output_file), exist_ok=True)
processed_df.to_csv(output_file, index=False)

print(f"✅ Processed Data Saved at: {output_file}")

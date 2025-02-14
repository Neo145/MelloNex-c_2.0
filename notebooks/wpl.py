import pandas as pd
import os

# Define file paths
input_file = r"F:\MelloNex-c 2.0\data\raw\Wpl 2023-2024.csv"
output_folder = r"F:\MelloNex-c 2.0\data\wpl"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the dataset
df = pd.read_csv(input_file)

# Handling missing values by filling them with 0
df['winner_runs'].fillna(0, inplace=True)
df['winner_wickets'].fillna(0, inplace=True)

# Splitting datasets
df_2023 = df[df['season'] == 2023]
df_2024 = df[df['season'] == 2024]
df_all = df.copy()

# Function to compute head-to-head statistics
def head_to_head_analysis(data):
    head_to_head = {}

    for _, row in data.iterrows():
        team1 = row['team1']
        team2 = row['team2']
        winner = row['winner']

        # Create keys for team1 vs team2 and vice versa
        matchup1 = (team1, team2)
        matchup2 = (team2, team1)

        if matchup1 not in head_to_head and matchup2 not in head_to_head:
            head_to_head[matchup1] = {"Total Matches": 0, team1: 0, team2: 0, "Draw": 0}

        matchup_key = matchup1 if matchup1 in head_to_head else matchup2

        # Update total matches count
        head_to_head[matchup_key]["Total Matches"] += 1

        # Update win/loss/draw count
        if winner == team1:
            head_to_head[matchup_key][team1] += 1
        elif winner == team2:
            head_to_head[matchup_key][team2] += 1
        else:
            head_to_head[matchup_key]["Draw"] += 1

    # Convert dictionary to DataFrame
    head_to_head_df = pd.DataFrame.from_dict(head_to_head, orient="index").reset_index()
    head_to_head_df.rename(columns={"index": "Matchup"}, inplace=True)

    return head_to_head_df

# Compute team vs team analysis for 2023, 2024, and all matches
h2h_2023 = head_to_head_analysis(df_2023)
h2h_2024 = head_to_head_analysis(df_2024)
h2h_all = head_to_head_analysis(df_all)

# Save the results
h2h_2023.to_csv(os.path.join(output_folder, "WPL_Head_to_Head_2023.csv"), index=False)
h2h_2024.to_csv(os.path.join(output_folder, "WPL_Head_to_Head_2024.csv"), index=False)
h2h_all.to_csv(os.path.join(output_folder, "WPL_Head_to_Head_All.csv"), index=False)

print("Head-to-head analysis completed. Results saved in:", output_folder)

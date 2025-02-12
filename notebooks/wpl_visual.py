import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# ✅ Set Matplotlib to use a non-GUI backend (Fixes Tkinter Issue)
import matplotlib
matplotlib.use('Agg')

# ✅ Define file paths
input_file = r"F:\MelloNex-c 2.0\data\processed\Wpl_Processed_Stats.csv"
output_dir = r"F:\MelloNex-c 2.0\src\visualization\dashboards"

# ✅ Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# ✅ Load the processed CSV file
df = pd.read_csv(input_file)

# ✅ Safely convert 'Match Years' column from string to list format
def safe_eval(value):
    """Safely converts string representation of lists into actual lists, handling NaN values."""
    try:
        return eval(value) if isinstance(value, str) and value.startswith("[") else []
    except:
        return []

df['Match Years'] = df['Match Years'].apply(safe_eval)

# ✅ **1️⃣ Bar Chart: Wins Comparison for All Teams**
plt.figure(figsize=(12, 6))
for team in df["Team"].unique():
    team_df = df[df["Team"] == team]
    plt.bar(team_df["Opponent"], team_df[f"{team} Wins"], label=team, alpha=0.7)

plt.xlabel("Opponent Teams")
plt.ylabel("Number of Wins")
plt.title("Head-to-Head Wins Comparison")
plt.xticks(rotation=45)
plt.legend(loc="upper right", bbox_to_anchor=(1.3, 1))
plt.tight_layout()

# ✅ Save the bar chart
output_path1 = os.path.join(output_dir, "team_wins_comparison.png")
plt.savefig(output_path1)
plt.close()

# ✅ **2️⃣ Heatmap: Toss Impact Analysis**
plt.figure(figsize=(10, 5))

# Select only numeric values for heatmap
toss_df = df[['Team', 'Opponent', 'Toss Wins', 'Toss Won & Match Won', 'Toss Won & Match Lost']].dropna()

# Ensure there's valid data for the heatmap
if not toss_df.empty:
    heatmap_data = toss_df.pivot(index="Team", columns="Opponent", values="Toss Won & Match Won")
    
    if heatmap_data.notnull().values.any():  # Check if the heatmap contains valid numbers
        sns.heatmap(heatmap_data, annot=True, cmap="Blues", fmt=".0f", linewidths=0.5)
        plt.title("Toss Wins Leading to Match Wins")
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        plt.tight_layout()

        # ✅ Save the heatmap
        output_path2 = os.path.join(output_dir, "toss_impact_heatmap.png")
        plt.savefig(output_path2)
        plt.close()
    else:
        print("⚠️ No valid data for heatmap. Skipping heatmap generation.")
        output_path2 = "No heatmap generated"
else:
    print("⚠️ Toss data is empty. Skipping heatmap generation.")
    output_path2 = "No heatmap generated"

# ✅ **3️⃣ Line Plot: Performance Over Years**
plt.figure(figsize=(12, 6))
for team in df["Team"].unique():
    team_df = df[df["Team"] == team]
    years = sorted(set(y for sublist in team_df["Match Years"] for y in sublist))
    matches = [sum(y in sublist for sublist in team_df["Match Years"]) for y in years]

    if years:  # Ensure there is valid data
        plt.plot(years, matches, marker="o", label=team)

plt.xlabel("Year")
plt.ylabel("Total Matches Played")
plt.title("Team Performance Over Years")
plt.xticks(years)
plt.legend()
plt.grid(True)
plt.tight_layout()

# ✅ Save the line plot
output_path3 = os.path.join(output_dir, "performance_over_years.png")
plt.savefig(output_path3)
plt.close()

# ✅ Print saved file paths
print(f"✅ Visualization saved at:\n{output_path1}\n{output_path2}\n{output_path3}")

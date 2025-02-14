import pandas as pd
import os

def calculate_head_to_head(df, season=None):
    if season:
        df = df[df['season'] == season]
    
    head_to_head = {}
    
    for _, row in df.iterrows():
        team1, team2 = row['team1'], row['team2']
        winner = row['winner']
        
        teams = tuple(sorted([team1, team2]))
        
        if teams not in head_to_head:
            head_to_head[teams] = {'matches': 0, team1: 0, team2: 0, 'draws': 0}
        
        head_to_head[teams]['matches'] += 1
        
        if pd.isna(winner) or winner not in [team1, team2]:
            head_to_head[teams]['draws'] += 1
        else:
            head_to_head[teams][winner] += 1
    
    return head_to_head

def restructure_h2h_dataframe(h2h_dict):
    h2h_list = []
    for teams, stats in h2h_dict.items():
        team1, team2 = teams
        h2h_list.append({
            'Team 1': team1,
            'Team 2': team2,
            'Matches Played': stats['matches'],
            'Team 1 Wins': stats[team1],
            'Team 2 Wins': stats[team2],
            'Draws': stats['draws']
        })
    return pd.DataFrame(h2h_list)

def analyze_toss_decision(df, season=None):
    if season:
        df = df[df['season'] == season]

    toss_analysis_list = []

    for _, row in df.iterrows():
        match_no = row['match_number']
        match_details = f"{row['team1']} vs {row['team2']}"
        toss_winner = row['toss_winner']
        toss_decision = row['toss_decision']
        match_winner = row['winner']

        toss_success = "Success" if toss_winner == match_winner else "Fail"

        toss_analysis_list.append({
            'Match No': match_no,
            'Match': match_details,
            'Toss Won By': toss_winner,
            'Toss Decision': toss_decision,
            'Match Won By': match_winner,
            'Toss Decision Success/Fail': toss_success
        })

    return pd.DataFrame(toss_analysis_list)

def analyze_match_results(df, season=None):
    if season:
        df = df[df['season'] == season]

    df['Win Type'] = df.apply(lambda row: 'Chasing' if 
                              ((row['toss_decision'] == 'field' and row['winner'] != row['toss_winner']) or
                               (row['toss_decision'] == 'bat' and row['winner'] == row['toss_winner'])) 
                              else 'Batting First', axis=1)

    return df.groupby(['season', 'Win Type']).size().unstack(fill_value=0)

def process_wpl_data(input_file, output_folder):
    df = pd.read_csv(input_file)
    
    overall_h2h = calculate_head_to_head(df)
    h2h_2023 = calculate_head_to_head(df, season=2023)
    h2h_2024 = calculate_head_to_head(df, season=2024)
    
    overall_h2h_df = restructure_h2h_dataframe(overall_h2h)
    season_2023_h2h_df = restructure_h2h_dataframe(h2h_2023)
    season_2024_h2h_df = restructure_h2h_dataframe(h2h_2024)
    
    overall_toss_decision_df = analyze_toss_decision(df)
    toss_decision_2023_df = analyze_toss_decision(df, season=2023)
    toss_decision_2024_df = analyze_toss_decision(df, season=2024)
    
    match_results_df = analyze_match_results(df)
    
    os.makedirs(output_folder, exist_ok=True)
    overall_h2h_df.to_csv(os.path.join(output_folder, 'overall_wpl_h2h.csv'), index=False)
    season_2023_h2h_df.to_csv(os.path.join(output_folder, '2023_wpl_h2h.csv'), index=False)
    season_2024_h2h_df.to_csv(os.path.join(output_folder, '2024_wpl_h2h.csv'), index=False)
    
    overall_toss_decision_df.to_csv(os.path.join(output_folder, 'overall_toss_decision.csv'), index=False)
    toss_decision_2023_df.to_csv(os.path.join(output_folder, '2023_toss_decision.csv'), index=False)
    toss_decision_2024_df.to_csv(os.path.join(output_folder, '2024_toss_decision.csv'), index=False)
    
    match_results_df.to_csv(os.path.join(output_folder, 'match_results_analysis.csv'))
    
    print("Processing complete. Files saved in", output_folder)

if __name__ == "__main__":
    input_file_path = "F:\\MelloNex-c 2.0\\data\\raw\\Wpl 2023-2024.csv"
    output_file_path = "F:\\MelloNex-c 2.0\\data\\external"
    
    process_wpl_data(input_file_path, output_file_path)

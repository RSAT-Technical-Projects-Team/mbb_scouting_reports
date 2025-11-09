""" Generates player_report section given functions from shot_dist.py and the_who.py """
import difflib

import shot_dist.get_df as shot_dist #include when ready
import the_who.get_df as the_who
import four_factors.get_df as four_factors

import pandas as pd
import gspread

def generate_reports(player_df : pd.DataFrame,  team_df : pd.DataFrame,
                     team_name : str, title : str) -> None:
    """
    Takes dataframes generated from shot_dist and the_who functions and connects to google drive
    to automatically fill in the report

    Parameters
    ---------
        player_df : pd.DataFrame
            A dataframe describing the player data dump from CBBAnalytics
        team_df : pd.DataFrame
            A dataframe describing the team data dump from CBBAnalytics
        team_name : str
            The opposing team name
        title : str
            The title of the report
    """

    team_id = team_df.loc[team_df['teamMarket'] == team_name, 'teamId'].values[0]
    shot_dist_df = shot_dist.get_shot_dist_df(player_df, team_id)
    who_to_foul = the_who.get_who_to_foul(player_df, team_id)
    who_draws_fouls = the_who.get_who_draws_fouls(player_df, team_id)
    who_turnsover = the_who.get_who_turnsover(player_df, team_id)
    who_3p = the_who.get_3p_shooters(player_df, team_id)

    who_rim = the_who.get_rim_finishers(player_df, team_id)
    who_orb = the_who.get_who_orb(player_df, team_id)

    #four_facts_df = four_factors.get_four_factors_df(team_df, team_id)

    gc = gspread.oauth(
        credentials_filename="gspread_user/gspread_auth/credentials.json",
        authorized_user_filename="gspread_user/gspread_auth/authorized_user.json"
    )
    gc_url = "https://docs.google.com/spreadsheets/d/1ItBPiRC8oAw9ca2RSwYjePAYbfe_I0juqLAOnZxyj0s/edit?gid=930660395#gid=930660395"
    sh = gc.open_by_url(gc_url)

    starting_cols = {
    0: ["A", "H"],
    1: ["J", "Q"]
    }
    def series_to_list(series):
        return series.to_numpy().reshape(-1,1).tolist()
    starting_rows = dict(zip([0,1,2], [[65 + n, 68 + n] for n in [0,6, 13]]))
    #finds template sheet, then duplicates, ID: 103706
    template = [sheet for sheet in sh.worksheets() if
                sheet.title == "DONT EDIT -- MBB Game Template 25-26"][0]
    template = template.duplicate(new_sheet_name = title)
    who_dfs = [[who_to_foul, who_turnsover, who_3p], [who_draws_fouls, who_rim, who_orb]]
    for idx_1 in range(2):
        col_1, col_2 = starting_cols[idx_1]
        for idx_2 in range(3):
            starting_row = starting_rows[idx_2]
            df = who_dfs[idx_1][idx_2].fillna(0)
            template.update(series_to_list(df[df.columns[0]]),
                            f"{col_1}{starting_row[0]}:{col_1}{starting_row[1]}")
            template.update(series_to_list(df[df.columns[-1]]),
                            f"{col_2}{starting_row[0]}:{col_2}{starting_row[1]}")
            if len(df.columns) > 2:
                template.update(series_to_list(df[df.columns[1]]),
                            "G78:G81")
    shot_dist_matrix = shot_dist_df.to_numpy().tolist()
    template.update(shot_dist_matrix, "D90:N107")

def main():
    """
    Sample main function which currently is the way our user interacts with the program
    """
    team_name = input("Input Team Name: ")
    date = input("Input Date: ")
    player_df = pd.read_csv("../sample_data/D1_PlayerBox.csv")
    team_df = pd.read_csv("../sample_data/D1_TeamFourFact.csv")
    team_name = difflib.get_close_matches(team_name, team_df['teamMarket'].tolist(), n=1)[0]
    title = f"{date} - {team_name}"
    print(f"Generating Report {title}")
    generate_reports(player_df, team_df, team_name, title)
if __name__ == "__main__":
    main()

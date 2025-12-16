""" Generates player_report section given functions from shot_dist.py and the_who.py """
import difflib

import shot_dist.get_df as shot_dist #include when ready
import the_who.get_df as the_who
import four_factors.get_df as four_factors

import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

from get_data.get_data import build_playerbox, build_fourfacts, fetch_espn_data

def generate_reports(player_df : pd.DataFrame,  team_df : pd.DataFrame,
                     team_id : str, team_name : str, date : str, uses_espn : bool) -> None:
    """
    Takes dataframes generated from shot_dist and the_who functions and connects to google drive
    to automatically fill in the report

    Parameters
    ---------
        player_df : pd.DataFrame
            A dataframe describing the player data dump from CBBAnalytics
        team_df : pd.DataFrame
            A dataframe describing the team data dump from CBBAnalytics
        team_id : str
            The opposing team id
        team_name : str
            Opposing team name
        date : str
            The date of the game
        uses_espn : bool
            Whether the data was pulled from ESPN or CBBAnalytics
    """

    month_day = date.rsplit("/", 1)[0]
    team_name_short = team_name.split()[0]
    title = f"{month_day} - {team_name_short}"
    print(f"Generating Report {title}")
    shot_dist_df = shot_dist.get_shot_dist_df(player_df, team_id, uses_espn)
    who_to_foul = the_who.get_who_to_foul(player_df, team_id)
    who_draws_fouls = the_who.get_who_draws_fouls(player_df, team_id)
    who_turnsover = the_who.get_who_turnsover(player_df, team_id)
    who_3p = the_who.get_3p_shooters(player_df, team_id)

    who_rim = the_who.get_rim_finishers(player_df, team_id)
    who_orb = the_who.get_who_orb(player_df, team_id)

    four_fact = four_factors.get_four_factors_df(team_df, team_id, uses_espn)


    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = Credentials.from_service_account_file("gspread_user/gspread_auth/service_account.json", scopes=scopes)
    gc = gspread.authorize(creds)

    gc_url = "https://docs.google.com/spreadsheets/d/1ItBPiRC8oAw9ca2RSwYjePAYbfe_I0juqLAOnZxyj0s/edit?gid=976552522#gid=976552522"
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

    str_date = pd.to_datetime(date).strftime("%A, %B %d, %Y")
    template.update([[f"Rice v {team_name.split()[0]}"]], "E2:K2")
    template.update([[str_date]], "E4:K4")
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

    four_fact_matrix = four_fact.to_numpy().tolist()
    template.update(four_fact_matrix, "G12:N27")

def main():
    """
    Sample main function which currently is the way our user interacts with the program
    """
    team_name = input("Input Team Name: ")
    date = input("Input Date (m/d/y): ")
    uses_espn = input("Use ESPN Data? (y/n): ") == "y"
    if len(date.split("/")) != 3:
        print("Date must be in m/d/y format")
        return
    m, _, y = date.split("/")

    if m in ["11", "12"]:
        season = int(y) + 1
    else:
        season = int(y)

    if uses_espn:
        p_data, t_data, pbp = fetch_espn_data(season)
        player_df = build_playerbox(p_data, pbp)
        team_df = build_fourfacts(t_data, pbp)
        team_name = difflib.get_close_matches(team_name, player_df['full_team_name'].tolist(), n=1, cutoff = 0)[0]
        team_id = player_df.loc[player_df['full_team_name'] == team_name, 'teamId'].values[0]
    else:
        player_df = pd.read_csv("../sample_data/D1_PlayerBox.csv")
        team_df = pd.read_csv("../sample_data/D1_TeamFourFact.csv")
        team_name = difflib.get_close_matches(team_name, team_df['teamMarket'].tolist(), n=1)[0]
        team_id = team_df.loc[team_df['teamMarket'] == team_name, 'teamId'].values[0]

    generate_reports(player_df, team_df, team_id, team_name, date, uses_espn)
if __name__ == "__main__":
    main()

""" Generates player_report section given functions from shot_dist.py and the_who.py """
import shot_dist.get_df as shot_dist
import the_who.get_df as the_who
import four_factors.get_df as four_factors

import pandas as pd
import gspread

def generate_reports(player_df : pd.DataFrame,  team_df : pd.DataFrame,
                     team_id : int) -> None:
    """
    Takes dataframes generated from shot_dist and the_who functions and connects to google drive
    to automatically fill in the report

    Parameters
    ---------
        player_df : pd.DataFrame
            A dataframe describing the player data dump from CBBAnalytics
        team_df : pd.DataFrame
            A dataframe describing the team data dump from CBBAnalytics
        team_id : int
            The opposing team id
    """

    shot_dist_df = shot_dist.get_shot_dist_df(player_df, team_id)

    who_to_foul = the_who.get_who_to_foul(player_df, team_id)
    who_draws_fouls = the_who.get_who_draws_fouls(player_df, team_id)
    who_turnsover = the_who.get_who_turnsover(player_df, team_id)
    who_3p = the_who.get_3p_shooters(player_df, team_id)
    who_orb = the_who.get_who_orb(player_df, team_id)

    four_facts_df = four_factors.get_four_factors_df(team_df, team_id)

    gc = gspread.oauth(
        credentials_filename="gspread_auth/credentials.json",
        authorized_user_filename="gspread_auth/authorized_user.json",
    )

    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ItBPiRC8oAw9ca2RSwYjePAYbfe_I0juqLAOnZxyj0s/edit?gid=930660395#gid=930660395')

    #finds template sheet, then duplicates
    template = [sheet for sheet in sh.worksheets() if 
                sheet.title == "Sample_Report"][0]
    
    #TODO: Update template with our dfs


def main():
    """
    Sample main function which currently is the way our user interacts with the program
    """
    team_id = input("Input Team ID")
    player_df = pd.read_csv("sample_data/D1_PlayerBox.csv")
    team_df = pd.read_csv("sample_data/D1_TeamFourFact.csv")
    generate_reports(player_df, team_df, team_id)

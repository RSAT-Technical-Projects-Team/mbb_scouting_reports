""" Functions which generate the shot distribution part of the mbb scouting report """
import pandas as pd
import numpy as np

def get_shot_dist_df(df : pd.DataFrame, team_id : int) -> pd.DataFrame:
    """
    Builds a dataframe from a raw data dump in the following style, describing the shot distributions for the opposing team:

    +---------------+--------+---------+------+-----------+--------+---------+--------+-----------------+-------------------+
    | Number/Player | FGA/G  | FT Rate | FT%  | Rim Rate  | Rim%   | 3s Rate | 3s%    | Mid-Range Rate  | Mid-Range FG%     |
    +===============+========+=========+======+===========+========+=========+========+=================+===================+
    |#Num Full Name |        |         |      |           |        |         |        |                 |                   |
    +---------------+--------+---------+------+-----------+--------+---------+--------+-----------------+-------------------+
    |               |        |         |      |           |        |         |        |                 |                   |
    +---------------+--------+---------+------+-----------+--------+---------+--------+-----------------+-------------------+
    |               |        |         |      |           |        |         |        |                 |                   |
    +---------------+--------+---------+------+-----------+--------+---------+--------+-----------------+-------------------+
    |               |        |         |      |           |        |         |        |                 |                   |
    +---------------+--------+---------+------+-----------+--------+---------+--------+-----------------+-------------------+
    |               |        |         |      |           |        |         |        |                 |                   |
    +---------------+--------+---------+------+-----------+--------+---------+--------+-----------------+-------------------+
    |               |        |         |      |           |        |         |        |                 |                   |
    +---------------+--------+---------+------+-----------+--------+---------+--------+-----------------+-------------------+
    |               |        |         |      |           |        |         |        |                 |                   |
    +---------------+--------+---------+------+-----------+--------+---------+--------+-----------------+-------------------+
    |               |        |         |      |           |        |         |        |                 |                   |
    +---------------+--------+---------+------+-----------+--------+---------+--------+-----------------+-------------------+
    |               |        |         |      |           |        |         |        |                 |                   |
    +---------------+--------+---------+------+-----------+--------+---------+--------+-----------------+-------------------+

    Parameters
    ---------
        df: pd.Dataframe
            The dataframe describing the data dump from CBBAnalytics
        team_id : int
            The opposing team's id
    
    Returns
    -------
        pd.Dataframe
            A dataframe describing the shot distribution chart
    """
    opp = df.loc[df["teamId"] == team_id].copy()
    opp["Rim Rate"] = np.nan #Cannot seem to find these...
    opp["Rim%"] = np.nan
    opp["Mid-Range Rate"] = np.nan
    opp["Mid-Range FG%"] = np.nan

    output = pd.DataFrame({
        "Number/Player": "#" + opp["jerseyNum"].astype(str) + " " + opp["fullName"].astype(str),
        "Number/Player_2": "#" + opp["jerseyNum"].astype(str) + " " + opp["fullName"].astype(str),
        "FGA/G": opp["fgaPg"],
        "FT Rate": opp["ftaRate"],
        "FT%": opp["ftPct"],
        "Rim Rate": opp["Rim Rate"],
        "Rim%": opp["Rim%"],
        "3s Rate": opp["fga3Rate"],
        "3s%": opp["fg3Pct"],
        "Mid-Range Rate": opp["Mid-Range Rate"],
        "Mid-Range FG%": opp["Mid-Range FG%"],
    }).sort_values(by = "Number/Player")
    output = output.fillna("N/A")
    output = pd.concat([output, output], ignore_index=True).sort_values(by = "FGA/G", ascending = False).reset_index(drop=True)
    if output.shape[0] > 18:
        output = output.tail(18)
    return output

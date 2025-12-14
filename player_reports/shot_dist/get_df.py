""" Functions which generate the shot distribution part of the mbb scouting report """
import pandas as pd
import numpy as np

def get_shot_dist_df(df : pd.DataFrame, team_id : int, espn : bool) -> pd.DataFrame:
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
        espn : bool
            Whether the data was pulled from ESPN or CBBAnalytics
    
    Returns
    -------
        pd.Dataframe
            A dataframe describing the shot distribution chart
    """
    opp = df.loc[df["teamId"] == team_id].copy()
    if not espn:
        opp['RimRate'] = np.nan
        opp['rimFG'] = np.nan
        opp['MidRate'] = np.nan
        opp['midFG'] = np.nan

    output = pd.DataFrame({
        "Number/Player": "#" + opp["jerseyNum"].astype(str) + " " + opp["fullName"].astype(str),
        "Number/Player_2": "#" + opp["jerseyNum"].astype(str) + " " + opp["fullName"].astype(str),
        "FGA/G": opp["fgaPg"],
        "FT Rate": opp["ftaRate"],
        "FT%": opp["ftPct"],
        "Rim Rate": opp["RimRate"],
        "Rim%": opp["rimFG"],
        "3s Rate": opp["fga3Rate"],
        "3s%": opp["fg3Pct"],
        "Mid-Range Rate": opp["MidRate"],
        "Mid-Range FG%": opp["midFG"],
    }).sort_values(by = "Number/Player")
    output = output.fillna(-1)
    output = pd.concat([output, output], ignore_index=True).sort_values(by = "FGA/G", ascending = False).reset_index(drop=True)
    if output.shape[0] > 18:
        output = output.tail(18)
    return output

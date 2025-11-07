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

    opp["3s Rate"] = np.where(
        (opp["fga"] > 0) & (opp["fga3"] > 0),  # require some 3PA
        opp["fga3"]/opp["fga"],
        np.nan,
    )

    opp["3s%"] = np.where(
        opp["fga3"] > 0,
        opp["fgm3"]/opp["fga3"],
        np.nan,
    )

    opp["Rim Rate"] = np.nan
    opp["Rim%"] = np.nan
    opp["Mid-Range Rate"] = np.nan
    opp["Mid-Range FG%"] = np.nan

    output = pd.DataFrame({
        "Number/Player": "#" + opp["jerseyNum"].astype(str) + " " + opp["fullName"].astype(str),
        "FGA/G": opp["fgaPg"],
        "FT Rate": opp["ftARate"],
        "FT%": opp["ftPct"],
        "Rim Rate": opp["Rim Rate"],
        "Rim%": opp["Rim%"],
        "3s Rate": opp["3s Rate"],
        "3s%": opp["3s%"],
        "Mid-Range Rate": opp["Mid-Range Rate"],
        "Mid-Range FG%": opp["Mid-Range FG%"],
    })

    return output.fillna("N/A").reset_index(drop=True)

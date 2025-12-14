"""
Builds a dataframe from raw data for the four factors section 
"""
import pandas as pd

def get_four_factors_df(team_df : pd.DataFrame, team_id : int, espn : bool) -> pd.DataFrame:
    """
    Builds a dataframe from a raw data dump in the following style, describing the four factors for both
    Rice and the opposing team

    +--------------+----------------------+----------+------------+------+----------+------------+------+
    | Category     | Metric               | %        | Percentile | Opp  | %        | Percentile | Opp  |
    +==============+======================+==========+============+======+==========+============+======+
    | Four         | eFG%                 |          |            |      |          |            |      |
    | Factors      +----------------------+----------+------------+------+----------+------------+------+
    |              | TOV%                 |          |            |      |          |            |      |
    +--------------+----------------------+----------+------------+------+----------+------------+------+
    |              | ORB%                 |          |            |      |          |            |      |
    +--------------+----------------------+----------+------------+------+----------+------------+------+
    |              | FTA Rate             |          |            |      |          |            |      |
    +--------------+----------------------+----------+------------+------+----------+------------+------+
    | Shooting     | Rim                  |          |            |      |          |            |      |
    |              +----------------------+----------+------------+------+----------+------------+------+
    |              | FGA Rate             |          |            |      |          |            |      |
    +--------------+----------------------+----------+------------+------+----------+------------+------+
    |              | FG%                  |          |            |      |          |            |      |
    +--------------+----------------------+----------+------------+------+----------+------------+------+
    |              | Midrange             |          |            |      |          |            |      |
    |              +----------------------+----------+------------+------+----------+------------+------+
    |              | FGA Rate             |          |            |      |          |            |      |
    +--------------+----------------------+----------+------------+------+----------+------------+------+
    |              | FG%                  |          |            |      |          |            |      |
    +--------------+----------------------+----------+------------+------+----------+------------+------+
    |              | 3Pt                  |          |            |      |          |            |      |
    |              +----------------------+----------+------------+------+----------+------------+------+
    |              | FGA Rate             |          |            |      |          |            |      |
    +--------------+----------------------+----------+------------+------+----------+------------+------+
    |              | FG%                  |          |            |      |          |            |      |
    +--------------+----------------------+----------+------------+------+----------+------------+------+
    | Free Throws  | FT%                  |          |            |      |          |            |      |
    +--------------+----------------------+----------+------------+------+----------+------------+------+
    | Ball         | AST%                 |          |            |      |          |            |      |
    | Movement     |                      |          |            |      |          |            |      |
    +--------------+----------------------+----------+------------+------+----------+------------+------+
    | Defense      | STL%                 |          |            |      |          |            |      |
    +--------------+----------------------+----------+------------+------+----------+------------+------+
    |              | BLK%                 |          |            |      |          |            |      |
    +--------------+----------------------+----------+------------+------+----------+------------+------+
    | Transition   | % Shots              |          |            |      |          |            |      |
    +--------------+----------------------+----------+------------+------+----------+------------+------+
    |              | eFG%                 |          |            |      |          |            |      |
    +--------------+----------------------+----------+------------+------+----------+------------+------+


    Parameters
    ---------
        df: pd.Dataframe
            The dataframe describing the data dump from CBBAnalytics
        team_id : int
            The opposing team's id

    Returns
    -------
        pd.Dataframe
            A dataframe describing the four factors section
    """
    rice_id = 242 if espn else 104135 
    opponents = team_df.loc[team_df["teamId"] == team_id].copy()
    rice = team_df.loc[team_df["teamId"] == rice_id].copy() #just  rice numbers

    #efgPct, tovPct, ftaRate, fg3Rate, no rim and no midrange numbers, no transition numbers
    pct = ['efgPct', 'tovPct', 'orbPct', 'ftaRate',
              'rimrate', 'rimFG', 'midrate', 'midfg',
              'fga3Rate', 'fg3Pct','ftPct', 'astPct',
              'stlPct', 'blkPct', 'transition_rate', 'transition_efg']
    pctile_list = pct.copy()
    pctile_list[5] = "fga3Rate"
    pctile_list[7] = "fga3Rate"
    pctile_list[9] = "fga3Rate"
    pctile_list[15] = "transition_rate"
    tile = [x + "Pctile" for x in pctile_list]
    agst = ["opp_" + x for x in pct]
    agst_pct = ["opp_" +  x + "Pctile" for x in pctile_list]


    # can do the four factors, defense, and transition
    # percentile stats have Pctile ending, Agst is opponent numbers, AgstPctile is percentile for opponent

    result_df = pd.DataFrame(
        {
            "Opp %": opponents.reindex(columns=pct).iloc[0].tolist(),
            "Opp Percentile": opponents.reindex(columns=tile).iloc[0].tolist(),
            "Opp Agst": opponents.reindex(columns=agst).iloc[0].tolist(),
            "Opp Agst_Pct": opponents.reindex(columns=agst_pct).iloc[0].tolist(),
            "Rice %": rice.reindex(columns=pct).iloc[0].tolist(),
            "Rice Percentile": rice.reindex(columns=tile).iloc[0].tolist(),
            "Rice Agst": rice.reindex(columns=agst).iloc[0].tolist(),
            "Rice Agst_Pct": rice.reindex(columns=agst_pct).iloc[0].tolist(),
        }
    )
    result_df = result_df.fillna(-1)
    result_df = result_df.mul(100).round(2)

    return result_df

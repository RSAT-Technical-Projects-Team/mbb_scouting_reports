""" Functions which generate "The Who" part of the mbb scouting report """
import pandas as pd

def get_who_to_foul(df : pd.DataFrame, team_id : int) -> pd.DataFrame:
    """
    Builds the "Who to Foul" Section, describing the top fourth worst FT% shooters
    Ordered from worst to best.

    Should look like:
    +-------------------------------------------+------+
    | Who To Foul: (Order best to 4th best)     | FT%  |
    +===========================================+======+
    |#Number Full Name                          |      |
    +-------------------------------------------+------+
    |                                           |      |
    +-------------------------------------------+------+
    |                                           |      |
    +-------------------------------------------+------+
    |                                           |      |
    +-------------------------------------------+------+

    Parameters
    ---------
        df: pd.Dataframe
            The dataframe describing the data dump from CBBAnalytics
        team_id : int
            The opposing team's id
    
    Returns
    -------
        pd.Dataframe
            A dataframe describing the who to foul section
    """
    opponents = df.loc[(df['teamId'] == team_id), ['jerseyNum', 'fullName', 'ftPct']]
    who_foul = opponents.sort_values(by=['ftPct'], ascending=True).head(4)
    return who_foul

def get_who_draws_fouls(df : pd.DataFrame, team_id : int) -> pd.DataFrame:
    """
    Builds the "Who Draws Fouls" Section, describing the top foul drawers
    Ordered from worst to best.

    Should look like:
    +-------------------------------------------+---------+
    | Who Draws Fouls: (Order most to 4th most) | FTAs/g  |
    +=====================================================+
    |#Number Full Name                          |         |
    +-------------------------------------------+---------+
    |                                           |         |
    +-------------------------------------------+---------+
    |                                           |         |
    +-------------------------------------------+---------+
    |                                           |         |
    +-------------------------------------------+---------+

    Parameters
    ---------
        df: pd.Dataframe
            The dataframe describing the data dump from CBBAnalytics
        team_id : int
            The opposing team's id
    
    Returns
    -------
        pd.Dataframe
            A dataframe describing the who to foul section
    """
    return pd.DataFrame()

def get_who_turnsover(df : pd.DataFrame, team_id : int) -> pd.DataFrame:
    """
    Builds the "Who Turns Over" Section, describing the top four worst in TO/Game
    Ordered from worst to best.

    Should look like:
    +----------------------------------------------------+----------+
    | Who Turns the Ball Over: (Order worst to 4th worst)| TOV/Game |
    +====================================================+==========+
    |#Number Full Name                                   |          |
    +----------------------------------------------------+----------+
    |                                                    |          |
    +----------------------------------------------------+----------+
    |                                                    |          | 
    +----------------------------------------------------+----------+
    |                                                    |          |
    +----------------------------------------------------+----------+

    Parameters
    ---------
        df: pd.Dataframe
            The dataframe describing the data dump from CBBAnalytics
        team_id : int
            The opposing team's id
    
    Returns
    -------
        pd.Dataframe
            A dataframe describing the turnover section
    """
    return pd.DataFrame()

def get_rim_finishers(df : pd.DataFrame, team_id : int) -> pd.DataFrame:
    """
    Builds the "Rim Finishers" Section, describing the Rim FG%
    Ordered from worst to best.

    Should look like:
    +-------------------------------------------+----------+
    | Rim Finishers: (Order Best to 4th best)   | Rim FG%  |
    +======================================================+
    |#Number Full Name                          |          |
    +-------------------------------------------+----------+
    |                                           |          |
    +-------------------------------------------+----------+
    |                                           |          |
    +-------------------------------------------+----------+
    |                                           |          |
    +-------------------------------------------+----------+

    Parameters
    ---------
        df: pd.Dataframe
            The dataframe describing the data dump from CBBAnalytics
        team_id : int
            The opposing team's id
    
    Returns
    -------
        pd.Dataframe
            A dataframe describing the rim finishers section
    """
    return pd.DataFrame()

def get_3p_shooters(df : pd.DataFrame, team_id : int) -> pd.DataFrame:
    """
    Builds the "3P Shooters" Section, describing the best 3P Shooters
    Ordered from worst to best 3FG%.

    Should look like:
    +-----------------------------------------------+----------+-------+
    | 3P Shooters: (Order best to 4th best)         | 3PA/game | 3FG% |
    +===============================================+==========+=======+
    |#Number Full Name                              |          |       |
    +-----------------------------------------------+----------+-------+
    |                                               |          |       |
    +-----------------------------------------------+----------+-------+
    |                                               |          |       |
    +-----------------------------------------------+----------+-------+
    |                                               |          |       |
    +-----------------------------------------------+----------+-------+


    Parameters
    ---------
        df: pd.Dataframe
            The dataframe describing the data dump from CBBAnalytics
        team_id : int
            The opposing team's id
    
    Returns
    -------
        pd.Dataframe
            A dataframe describing the 3P Shooters Section
    """

    return pd.DataFrame()

def get_who_orb(df : pd.DataFrame, team_id : int) -> pd.DataFrame:
    """
    Builds the "Who Grabs ORB" Section, best opposing players by ORBs/g
    Ordered from worst to best.

    Should look like:
    +------------------------------------+--------+
    | Who Grabs Offensive Boards:        | ORBs/g |
    +====================================+========+
    |#Number Full Name                   |        |
    +------------------------------------+--------+
    |                                    |        |
    +------------------------------------+--------+
    |                                    |        |
    +------------------------------------+--------+
    |                                    |        |
    +------------------------------------+--------+


    Parameters
    ---------
        df: pd.Dataframe
            The dataframe describing the data dump from CBBAnalytics
        team_id : int
            The opposing team's id
    
    Returns
    -------
        pd.Dataframe
            A dataframe describing the "Who Grabs ORB" Section
    """
    return pd.DataFrame()

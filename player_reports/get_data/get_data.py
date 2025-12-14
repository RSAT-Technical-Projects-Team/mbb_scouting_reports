""" 
Gets and cleans data from espn using sportsdataverse
"""
#TODO: Refactor!!! This is a mess. Also write documentation
import pandas as pd
import numpy as np
import sportsdataverse as sdv

def fetch_espn_data(year: int) -> pd.DataFrame:
    """
    Fetches ESPN data for the specified year using the sportsdataverse library.

    Parameters
    ---------
        year: int
            The season year for which to fetch the data.

    Returns
    -------
        pd.DataFrame
            A dataframe containing the ESPN data for the specified year.
    """
    t_data = sdv.mbb.load_mbb_team_boxscore(seasons=[year], return_as_pandas = True)
    p_data = sdv.mbb.load_mbb_player_boxscore(seasons=[year]).to_pandas()
    pbp = sdv.mbb.load_mbb_pbp(seasons=[year], return_as_pandas = True)

    pbp = pbp.dropna(subset = ['team_id'])
    pbp['opponent_team_id'] = np.where((pbp['team_id'] == pbp['home_team_id']), pbp['away_team_id'], pbp['home_team_id'])

    end_poss = ['Defensive Rebound', 'Lost Ball Turnover', 'End Period', 'RegularTimeOut', 'End Game', 'Technical Foul', 'MadeFreeThrow']

    pbp['2nd_ft'] = (pbp['type_text'] == 'MadeFreeThrow') & (pbp['type_text'].shift(1) == 'MadeFreeThrow')

    pbp['poss_change'] = ((pbp['type_text'].isin(end_poss) | (pbp['scoring_play'])) | (pbp['type_text'] == 'Steal') & (pbp['type_text'].shift(1) != 'Lost Ball Turnover')) & (~pbp['2nd_ft'])
    pbp['new_poss'] = (pbp['poss_change'].shift(1))

    pbp['rim_fga'] = (pbp['type_text'].isin(['LayUpShot', 'DunkShot', 'TipShot'])) & (pbp['score_value'] == 2)
    pbp['rim_fgm'] = pbp['rim_fga'] & (pbp['scoring_play'])
    pbp['mid_fga'] = (pbp['type_text'].isin(['JumpShot',])) & (pbp['score_value'] == 2)
    pbp['mid_fgm'] = pbp['mid_fga'] & (pbp['scoring_play'])
    return p_data, t_data, pbp


def build_playerbox(data : pd.DataFrame, pbp : pd.DataFrame) -> pd.DataFrame:
    """
    Builds the player boxscore dataframe for the given year.

    Parameters
    ---------
        data: pd.DataFrame
            The player boxscore data.
        

    Returns
    -------
        pd.DataFrame
            A dataframe containing the player boxscore data for the specified year.
    """
    
    
    player_df = data.groupby("athlete_id").agg(
            jerseyNum = ("athlete_jersey", "first"),
            fullName = ("athlete_display_name", "first"),
            teamId = ("team_id", "first"),
            team_location = ("team_location", "first"), 
            team_name = ("team_name", "first"), 
            games = ("game_id", "nunique"),
            fg_attempted_sum = ("field_goals_attempted", "sum"),
            fg_made_sum = ("field_goals_made", "sum"),
            free_throws_made_sum=("free_throws_made", "sum"),
            free_throws_attempted_sum=("free_throws_attempted", "sum"),
            three_pt_made_sum=("three_point_field_goals_made", "sum"),
            three_pt_att_sum=("three_point_field_goals_attempted", "sum"),
            turnovers_sum=("turnovers", "sum"),
            orb_sum=("offensive_rebounds", "sum")
        )
    player_df['two_point_made_sum'] = player_df['fg_made_sum'] - player_df['three_pt_made_sum']
    player_df['two_point_att_sum'] = (player_df['fg_attempted_sum'] - player_df['three_pt_att_sum'])

    player_df['fgaPg'] = player_df['fg_attempted_sum'] / player_df['games']
    player_df["ftaRate"] = player_df["free_throws_attempted_sum"] / player_df["fg_attempted_sum"]

    player_df['ftPct'] = player_df['free_throws_made_sum'] / player_df['free_throws_attempted_sum']
    player_df['fga3Rate'] = player_df['three_pt_att_sum'] / player_df['fg_attempted_sum']
    player_df['fg3Pct'] = player_df['three_pt_made_sum'] / player_df['three_pt_att_sum']
    player_df['fga3Pg'] = player_df['three_pt_att_sum'] / player_df['games']
    player_df["ftaPg"] = player_df["free_throws_attempted_sum"] / player_df["games"]

    player_df['tovPg'] = player_df['turnovers_sum'] / player_df['games']
    player_df['orbPg'] = player_df['orb_sum'] / player_df['games']

    player_df["fg2Pct"] = player_df['two_point_made_sum'] / player_df['two_point_att_sum']
    player_df['full_team_name'] = player_df['team_location'] + ' ' + player_df['team_name']

    shot_dist_special = pbp.groupby('athlete_id_1').agg(
        rim_fga_sum = ('rim_fga', 'sum'),
        rim_fgm_sum = ('rim_fgm', 'sum'),
        mid_fga_sum = ('mid_fga', 'sum'),
        mid_fgm_sum = ('mid_fgm', 'sum')
    )

    shot_dist_special['rimFG'] = shot_dist_special['rim_fgm_sum'] / (shot_dist_special['rim_fga_sum'])
    shot_dist_special['midFG'] = shot_dist_special['mid_fgm_sum'] / (shot_dist_special['mid_fga_sum'])

    player_df = pd.merge(player_df, shot_dist_special, left_index=True, right_index=True, how='left')
    den = player_df["fg_attempted_sum"].to_numpy()

    player_df["rimFG"] = np.divide(
        player_df["rim_fga_sum"].to_numpy(),
        den,
        out=np.zeros_like(den, dtype=float),
        where=den != 0
    )

    player_df["midFG"] = np.divide(
        player_df["mid_fga_sum"].to_numpy(),
        den,
        out=np.zeros_like(den, dtype=float),
        where=den != 0
    )

    player_df["RimRate"] = np.divide(
        player_df["rim_fga_sum"].to_numpy(),
        den,
        out=np.zeros_like(den, dtype=float),
        where=den != 0
    )

    player_df["MidRate"] = np.divide(
        player_df["mid_fga_sum"].to_numpy(),
        den,
        out=np.zeros_like(den, dtype=float),
        where=den != 0
    )

    player_df = player_df[['teamId', 'full_team_name', 'jerseyNum', 'fullName', 'games', 'fgaPg', 'ftaRate', 'ftPct', 'fga3Rate', 'fg3Pct', 'fga3Pg', 'ftaPg', 'tovPg', 'orbPg', 'fg2Pct', 'rimFG', 'RimRate', 'MidRate', 'midFG']].dropna()
    num_cols =  player_df.select_dtypes(include="number").columns
    player_df[num_cols] =  player_df[num_cols].round(4)
    return player_df

def build_fourfacts(box_score : pd.DataFrame, pbp : pd.DataFrame) -> pd.DataFrame:
    """ 
    Builds the four factors dataframe for the given year.
    """


    off_poss_count = pbp.groupby(['game_id', 'team_id', 'opponent_team_id'])[['new_poss', 'rim_fga', 'rim_fgm', 'mid_fga', 'mid_fgm']].sum().reset_index()
    off_poss_count = pd.merge(off_poss_count, off_poss_count, left_on = ['game_id', 'opponent_team_id'], right_on = ['game_id', 'team_id'], suffixes = ('', '_opp'))
    off_poss_count = off_poss_count.groupby('team_id')[['new_poss', 'rim_fga', 'rim_fgm', 'mid_fga', 'mid_fgm', 'new_poss_opp', 'rim_fga_opp', 'rim_fgm_opp', 'mid_fga_opp', 'mid_fgm_opp']].sum().reset_index()

    pbp['time_diff'] =  pd.to_datetime(pbp['wallclock']) - pd.to_datetime(pbp['wallclock'].shift(1))
    pbp['time_diff'] = pbp['time_diff'].dt.total_seconds()
    pbp['transition'] = (pbp['time_diff'] <= 8) & (pbp['time_diff'] >= 0) & (pbp['new_poss']) & (pbp['score_value'] > 1)

    transitions = pbp[pbp['transition']].copy()
    transitions['3pa'] = transitions['score_value'] == 3
    transitions['2pa'] = transitions['score_value'] == 2
    transitions['3pm'] = transitions['3pa'] & transitions['scoring_play']
    transitions['2pm'] = transitions['2pa'] & transitions['scoring_play']

    transition_stats = transitions.groupby(['game_id', 'team_id', 'opponent_team_id'])[['3pa', '3pm', '2pa', '2pm']].sum()
    transition_stats = transition_stats.add_suffix("_transition")
    transition_stats = transition_stats.reset_index()
    transition_stats = pd.merge(transition_stats, transition_stats, left_on=['game_id', 'opponent_team_id'], right_on=['game_id', 'team_id'], suffixes=('', '_opp'))
    transition_stats = transition_stats.groupby('team_id')[['3pa_transition', '3pm_transition', '2pa_transition', '2pm_transition',
                                        '3pa_transition_opp', '3pm_transition_opp', '2pa_transition_opp', '2pm_transition_opp']].sum().reset_index()

    m_data = box_score[['game_id', 'team_id', 'assists', 'blocks', 'defensive_rebounds',
       'fast_break_points', 'field_goal_pct', 'field_goals_made',
       'field_goals_attempted', 'flagrant_fouls', 'fouls', 'free_throw_pct',
       'free_throws_made', 'free_throws_attempted', 'largest_lead',
       'lead_changes', 'lead_percentage', 'offensive_rebounds',
       'points_in_paint', 'steals', 'team_turnovers', 'technical_fouls',
       'three_point_field_goal_pct', 'three_point_field_goals_made',
       'three_point_field_goals_attempted', 'total_rebounds',
       'total_technical_fouls', 'total_turnovers', 'turnover_points',
       'turnovers', 'opponent_team_id']]
    m_data = pd.merge(m_data, m_data, left_on=['game_id', 'opponent_team_id'], right_on=['game_id', 'team_id'], suffixes=('', '_opp'))

    basic_stats = m_data.groupby("team_id").agg(
        fg_attempted_sum = ("field_goals_attempted", "sum"),
        fg_made_sum = ("field_goals_made", "sum"),
        three_pt_made_sum=("three_point_field_goals_made", "sum"),
        three_pt_att_sum=("three_point_field_goals_attempted", "sum"),
        fta_sum=("free_throws_attempted", "sum"),
        ftm_sum=("free_throws_made", "sum"),
        to_sum=("turnovers", "sum"),
        orb_sum=("offensive_rebounds", "sum"),
        ast_sum = ("assists", "sum"),
        blk_sum = ("blocks", "sum"),
        stl_sum = ("steals", "sum"),
        fg_attempted_sum_opp = ("field_goals_attempted_opp", "sum")
    ).reset_index()

    team_stats = pd.merge(basic_stats, off_poss_count, on = 'team_id')
    team_stats = pd.merge(team_stats, transition_stats, on = 'team_id')

    new_cols = ['efgPct', 'tovPct', 'orbPct', 'ftaRate',
              'rimrate', 'rimFG', 'midrate', 'midfg',
              'fga3Rate', 'fg3Pct','ftPct', 'astPct',
              'stlPct', 'blkPct', 'transition_rate', 'transition_efg']

    team_stats['efgPct'] = (team_stats['fg_made_sum'] + 0.5 * team_stats['three_pt_made_sum']) / team_stats['fg_attempted_sum']
    team_stats['tovPct'] = team_stats['to_sum'] / team_stats['new_poss']
    team_stats['orbPct'] = team_stats['orb_sum'] / (team_stats['fg_attempted_sum'] - team_stats['fg_made_sum'])
    team_stats['ftaRate'] = team_stats['fta_sum'] / team_stats['fg_attempted_sum']
    team_stats['rimrate'] = team_stats['rim_fga'] / team_stats['fg_attempted_sum']
    team_stats['rimFG'] = team_stats['rim_fgm'] / team_stats['rim_fga']
    team_stats['midrate'] = team_stats['mid_fga'] / team_stats['fg_attempted_sum']
    team_stats['midfg'] = team_stats['mid_fgm'] / team_stats['mid_fga']
    team_stats['fga3Rate'] = team_stats['three_pt_att_sum'] / team_stats['fg_attempted_sum']
    team_stats['fg3Pct'] = team_stats['three_pt_made_sum'] / team_stats['three_pt_att_sum']

    team_stats['ftPct'] = team_stats['ftm_sum'] / team_stats['fta_sum']
    team_stats['astPct'] = team_stats['ast_sum'] / team_stats['fg_made_sum']
    team_stats['stlPct'] = team_stats['stl_sum'] / team_stats['new_poss_opp']
    team_stats['blkPct'] = team_stats['blk_sum'] / (team_stats['fg_attempted_sum_opp'])

    team_stats['transition_rate'] = (team_stats['2pa_transition'] + team_stats['3pa_transition']) / team_stats['fg_attempted_sum']
    team_stats['transition_efg'] = ((team_stats['2pm_transition'] + 1.5 * team_stats['3pm_transition']) / (team_stats['2pa_transition'] + team_stats['3pa_transition'])) / 100

    for col in new_cols:
        team_stats[f'{col}Pctile'] = team_stats[col].rank(pct=True)
    opp_sos_df = build_opp_stats_df(box_score, team_stats)
    for col in opp_sos_df.columns[1:]:
        opp_sos_df[f'{col}Pctile'] = opp_sos_df[col].rank(pct=True)
    opp_sos_df = opp_sos_df.add_prefix("opp_")
    opp_sos_df = opp_sos_df.rename(columns={"opp_team_id" : "teamId"})
    team_stats = team_stats.rename(columns={"team_id": "teamId"})

    four_facts = pd.merge(
        team_stats,
        opp_sos_df,
        on="teamId"
    )
    return four_facts

def agg_stats_sum(team_stats: pd.DataFrame) -> pd.Series:
    """ 
    Aggregates team statistics by summing them up.
    """
    s = team_stats.sum(numeric_only=True)

    def safe_div(num, den):
        return np.nan if den == 0 else num / den

    out = {
        "efgPct": safe_div(s["fg_made_sum"] + 0.5 * s["three_pt_made_sum"], s["fg_attempted_sum"]),
        "tovPct": safe_div(s["to_sum"], s["new_poss"]),
        "orbPct": safe_div(s["orb_sum"], (s["fg_attempted_sum"] - s["fg_made_sum"])),
        "ftaRate": safe_div(s["fta_sum"], s["fg_attempted_sum"]),
        "rimrate": safe_div(s["rim_fga"], s["fg_attempted_sum"]),
        "rimFG": safe_div(s["rim_fgm"], s["rim_fga"]),
        "midrate": safe_div(s["mid_fga"], s["fg_attempted_sum"]),
        "midfg": safe_div(s["mid_fgm"], s["mid_fga"]),
        "fga3Rate": safe_div(s["three_pt_att_sum"], s["fg_attempted_sum"]),
        "fg3Pct": safe_div(s["three_pt_made_sum"], s["three_pt_att_sum"]),
        "ftPct": safe_div(s["ftm_sum"], s["fta_sum"]),
        "astPct": safe_div(s["ast_sum"], s["fg_made_sum"]),
        "stlPct": safe_div(s["stl_sum"], s["new_poss_opp"]),
        "blkPct": safe_div(s["blk_sum"], s["fg_attempted_sum_opp"]),
        "transition_rate": safe_div(s["2pa_transition"] + s["3pa_transition"], s["fg_attempted_sum"]),
        "transition_efg": safe_div(s["2pm_transition"] + 1.5 * s["3pm_transition"],
                                   s["2pa_transition"] + s["3pa_transition"]),
    }

    return pd.Series(out)


def build_opp_stats_df(data : pd.DataFrame, four_facts: pd.DataFrame) -> pd.DataFrame:
    """
    Builds a DataFrame containing aggregated opponent statistics for each team.
    """

    sched = (
        data[["team_id", "opponent_team_id"]]
        .dropna()
        .drop_duplicates()
    )

    opp_map = sched.groupby("team_id")["opponent_team_id"].apply(set).to_dict()

    rows = []
    for team_id, opps in opp_map.items():
        opp_facts = four_facts[four_facts["team_id"].isin(opps)]
        metrics = agg_stats_sum(opp_facts)  # Series of one-number-per-metric

        row = {"team_id": team_id}
        row.update(metrics.to_dict())
        rows.append(row)

    return pd.DataFrame(rows)


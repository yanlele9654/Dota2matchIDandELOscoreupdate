import pandas as pd
def FBL_stats_win_cal(dataset):
    dire_FBL_stats = dataset.groupby(by='dire_team_id').sum()
    radiant_FBL_stats = dataset.groupby(by='radiant_team_id').sum()
    dire_FBL_stats = dire_FBL_stats.reset_index()
    radiant_FBL_stats = radiant_FBL_stats.reset_index()
    dire_FBL_stats = dire_FBL_stats.rename(
        columns={'dire_team_id': 'Team_id', 'dire_team': 'W_times', 'radiant_team': 'L_times'})
    radiant_FBL_stats = radiant_FBL_stats.rename(
        columns={'radiant_team_id': 'Team_id', 'dire_team': 'L_times', 'radiant_team': 'W_times'})
    Total_FBL_stats = pd.merge(dire_FBL_stats, radiant_FBL_stats, on='Team_id')
    Total_FBL_stats['W_total_times'] = Total_FBL_stats['W_times_x'] + Total_FBL_stats['W_times_y']
    Total_FBL_stats['L_total_times'] = Total_FBL_stats['L_times_x'] + Total_FBL_stats['L_times_y']
    Total_FBL_stats['Win_rate'] = Total_FBL_stats['W_total_times'] / (
                Total_FBL_stats['W_total_times'] + Total_FBL_stats['L_total_times'])
    Total_FBL_stats = Total_FBL_stats[['Team_id', 'Win_rate', 'W_total_times', 'L_total_times']]
    Total_FBL_stats['Total_times'] = Total_FBL_stats['W_total_times'] + Total_FBL_stats['L_total_times']

    Total_FBL_stats.Win_rate[Total_FBL_stats.Total_times < 10] = 0.5
    FBL_records_dict = Total_FBL_stats.to_dict('record')
    return FBL_records_dict

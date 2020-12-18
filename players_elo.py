import pandas as  pd
import pymongo

def team_id_match(Major_chongqing_major_Elo):
    dota_team_id = set(list(Major_chongqing_major_Elo.W_id) + list(Major_chongqing_major_Elo.L_id))

    dota_team_id = pd.DataFrame(list(dota_team_id))

    dota_team_id.index = dota_team_id[0]

    dota_team_id['team_id'] = range(len(dota_team_id))

    W_team_id = []
    L_team_id = []
    for i in range(len(Major_chongqing_major_Elo)):
        W_team_id.append(dota_team_id['team_id'][Major_chongqing_major_Elo['W_id'][i]])
        L_team_id.append(dota_team_id['team_id'][Major_chongqing_major_Elo['L_id'][i]])

    Major_chongqing_major_Elo['W_team_id'] = W_team_id
    Major_chongqing_major_Elo['L_team_id'] = L_team_id
    return (Major_chongqing_major_Elo)


import DataBaseAccess_c as DBA


db_eng_1 = DBA.DbInfoGenerator('vpgame').info
client = pymongo.MongoClient(db_eng_1['host'], 7974)
# 连接database'damin'
db = client['admin']
# 'admin'的账号密码
db.authenticate(db_eng_1['user'], db_eng_1['password'])
print('success connet the database')
dota_players_2018 = pd.read_csv('players_2018_info.csv')
dota_players_2019 = pd.read_csv('players_2019_info.csv')
dota_players_2020 = pd.DataFrame(list(db.players_2020.find(
    {}, {"match_id": 1, "account_id": 1, "win": 1, '_id': 0, 'start_time': 1})))
dota_players_total = dota_players_2019.append(dota_players_2020)
dota_players_total = dota_players_total.append(dota_players_2018)
dota_players_total = dota_players_total.sort_values(by=['start_time', 'match_id'])
dota_players_total = dota_players_total.reset_index(drop=True)
dota_players_total_win = dota_players_total[dota_players_total.win == 1]
dota_players_total_win = dota_players_total_win.reset_index(drop=True)
print('success get the player info')
W_id = []
W_account = []
for i in range(len(dota_players_total_win) - 1):
    if dota_players_total_win.match_id[i] == dota_players_total_win.match_id[i + 1]:
        W_id.append(dota_players_total_win.account_id[i])
    else:
        W_id.append(dota_players_total_win.account_id[i])
        W_account.append(W_id)
        W_id = []
dota_players_total_lose = dota_players_total[dota_players_total.win == 0]

dota_players_total_lose = dota_players_total_lose.reset_index(drop=True)
L_id = []
L_account = []
for i in range(len(dota_players_total_lose) - 1):
    if dota_players_total_lose.match_id[i] == dota_players_total_lose.match_id[i + 1]:
        L_id.append(dota_players_total_lose.account_id[i])
    else:
        L_id.append(dota_players_total_lose.account_id[i])
        L_account.append(L_id)
        L_id = []

match_id = dota_players_total_win.groupby('match_id')['match_id'].head(1)
match_id = match_id.reset_index(drop=True)
match_id = match_id.drop(match_id.index[-1])
match_id = list(match_id)

Winer_players = pd.DataFrame([match_id, W_account, L_account])
Winer_players = Winer_players.T
Winer_players.columns = ['match_id', 'W_account', 'L_account']

dota_stats1 = pd.read_csv('match_2018_info.csv')
dota_stats2 = pd.read_csv('match_2019_info.csv')
dota_stats3 = pd.DataFrame(list(db.dota_basic_data_2020.find({}, {
    'radiant_team_id': 1, 'dire_team_id': 1, 'radiant_win': 1, 'match_id': 1, 'leagueid': 1, '_id': 0,
    'start_time': 1, 'league.tier': 1, 'duration': 1, 'series_id': 1})))
print('success get the match info')


dota_stats1 = dota_stats1.append(dota_stats3)
dota_stats1 = dota_stats1.append(dota_stats2)
dota_stats1 = dota_stats1.dropna(subset=['match_id'])
dota_stats1[['match_id']] = dota_stats1[['match_id']].astype(int)
Winer_players['match_id'] = Winer_players['match_id'].astype(int)
dota_stats1 = pd.merge(Winer_players, dota_stats1, how="inner", on='match_id')

import itertools

W_team_players = list(itertools.chain.from_iterable(list(dota_stats1.W_account)))
L_team_players = list(itertools.chain.from_iterable(list(dota_stats1.L_account)))
W_team_players = list(map(lambda x: int(x), W_team_players))
L_team_players = list(map(lambda x: int(x), L_team_players))
total_players_id = pd.DataFrame(list(set(W_team_players + L_team_players)))
total_players_id.index = total_players_id[0]
total_players_id['players_id'] = range(len(total_players_id))
dota_stats1 = dota_stats1.dropna(subset=['duration', 'dire_team_id', 'radiant_team_id'])
dota_stats1 = dota_stats1.reset_index(drop=True)

W_player_1 = []
L_player_1 = []
W_player_2 = []
L_player_2 = []
W_player_3 = []
L_player_3 = []
W_player_4 = []
L_player_4 = []
W_player_5 = []
L_player_5 = []

for i in range(len(dota_stats1)):
    W_player_1.append(total_players_id['players_id'][dota_stats1['W_account'][i][0]])
    L_player_1.append(total_players_id['players_id'][dota_stats1['L_account'][i][0]])
    W_player_2.append(total_players_id['players_id'][dota_stats1['W_account'][i][1]])
    L_player_2.append(total_players_id['players_id'][dota_stats1['L_account'][i][1]])
    W_player_3.append(total_players_id['players_id'][dota_stats1['W_account'][i][2]])
    L_player_3.append(total_players_id['players_id'][dota_stats1['L_account'][i][2]])
    W_player_4.append(total_players_id['players_id'][dota_stats1['W_account'][i][3]])
    L_player_4.append(total_players_id['players_id'][dota_stats1['L_account'][i][3]])
    W_player_5.append(total_players_id['players_id'][dota_stats1['W_account'][i][4]])
    L_player_5.append(total_players_id['players_id'][dota_stats1['L_account'][i][4]])
dota_stats1['W_players_1'] = W_player_1
dota_stats1['L_players_1'] = L_player_1
dota_stats1['W_players_2'] = W_player_2
dota_stats1['L_players_2'] = L_player_2
dota_stats1['W_players_3'] = W_player_3
dota_stats1['L_players_3'] = L_player_3
dota_stats1['W_players_4'] = W_player_4
dota_stats1['L_players_4'] = L_player_4
dota_stats1['W_players_5'] = W_player_5
dota_stats1['L_players_5'] = L_player_5

dota_stats1.sort_values(by=['start_time'], inplace=True)

dire_team_id = []
radiant_team_id = []
for row in dota_stats1.itertuples():
    dire_team_id.append(row.dire_team_id)  # 在转换的时候把整个dire_team当作一个string的类型了
    radiant_team_id.append(row.radiant_team_id)
dota_stats1['dire_team'] = dire_team_id
dota_stats1['radiant_team'] = radiant_team_id


## ELO评分team
dota_stats1 = dota_stats1.reset_index(drop=True)
W_id = []
L_id = []
#    League_tier = []
for i in range(len(dota_stats1)):
    #    League_tier.append(dota_stats1['league'][i]['tier'])
    if dota_stats1['radiant_win'][i] == 0:
        W_id.append(int(dota_stats1['dire_team'][i]))
        L_id.append(int(dota_stats1['radiant_team'][i]))
    else:
        W_id.append(int(dota_stats1['radiant_team'][i]))
        L_id.append(int(dota_stats1['dire_team'][i]))
dota_stats1['W_id'] = W_id
dota_stats1['L_id'] = L_id

# dota_stats1['tier'] = League_tier

dota_stats1 = team_id_match(dota_stats1)
import elo_player as elo_player
elo_player = elo_player.elo_player()

dota_stats1_elo, dota_stats1_counted, current_team_change, one_month_played_times, players_individual_elo = elo_player.player_team_elo_result(dota_stats1, total_players_id, 16)
print('success calculator the new elo score')
dota_team_id = set(list(dota_stats1.W_id) + list(dota_stats1.L_id))
dota_team_id = pd.DataFrame(list(dota_team_id))

dota_team_id.index = dota_team_id[0]

dota_team_id['team_id'] = range(len(dota_team_id))

dota_team_id.rename(columns={0: 'Team_id'}, inplace=True)

dota_team_id['elo_score'] = dota_stats1_elo
dota_team_id['played_times'] = dota_stats1_counted
dota_team_id['last_change'] = current_team_change
dota_team_id['one_month_played'] = one_month_played_times
records1 = dota_team_id.to_dict('records')
db.player_Team_elo.drop()
db.player_Team_elo.insert_many(records1)
print(players_individual_elo[1])
client.close()
#%%
total_players_id['elo_score']=players_individual_elo
total_players_id=total_players_id.set_index(['players_id'])
total_players_id=total_players_id.reset_index(drop=True)
total_players_id.rename(columns={0:'account_id'},inplace=True)
records_players = total_players_id.to_dict('records')
db.dota2_players_elo.insert_many(records_players)
# %%
# %%

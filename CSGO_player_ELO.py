import pandas as pd
import pymongo
import DataBaseAccess_c as DBA 

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

db_eng_1 = DBA.DbInfoGenerator('vpgame').info
client = pymongo.MongoClient(db_eng_1['host'], 7974)
# 连接database'damin'
db = client['admin']
# 'admin'的账号密码
db.authenticate(db_eng_1['user'], db_eng_1['password'])
print('success connet the database')
csgo_players_info = pd.DataFrame(list(db.players_2020.find(
    {}, {"match_id": 1, "name": 1, '_id': 0, 'team_id':1})))

# 提取出csgo比赛数据结果，然后通过BO3,BO5,BO1,BO2等多个比赛进行分组，整体来说将player与比赛结果相匹配，整体的做法与CSGO_ELO_score相类似，可以参考Calculate_ELO_score来完成，整体的数据架构比较负责，可能需要结合多个mongodb的数据表来完成任务。

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
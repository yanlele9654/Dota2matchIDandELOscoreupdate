import pandas as pd
import pymongo
import DataBaseAccess_c as DBA
import elo
import elo_team
import imp

imp.reload(elo_team)
# %%
# 连接到本地库
db_eng_1 = DBA.DbInfoGenerator('vpgame').info

# 连接到数据库
match_client = pymongo.MongoClient(db_eng_1['host'], 7974)

# 连接database'damin'
match_db = match_client['admin']
# 'admin'的账号密码
match_db.authenticate(db_eng_1['user'], db_eng_1['password'])

# %%
# 获取比赛结果
# %%
# 获取比赛结果
match_result = pd.DataFrame(
    list(match_db.CSGO_Result.find({}, {'team1.id': 1, 'team2.id': 1, '_id': 0, 'result': 1, 'date': 1, 'format': 1})))


# %%
match_result = match_result.sort_values(by='date', ascending=True)
match_result = match_result.reset_index(drop=True)
for i in range(len(match_result)):
    team1_id = match_result['team1'][i]['id']
    team2_id = match_result['team2'][i]['id']
    match_result.at[i, 'team1'] = team1_id
    match_result.at[i, 'team2'] = team2_id
    team1_result = match_result['result'][i][0]
    team2_result = match_result['result'][i][-1]
    match_result.at[i, 'team1_result'] = team1_result
    match_result.at[i, 'team2_result'] = team2_result
# %%
match_result_BO1=match_result[match_result.format=='bo1']
match_result_BO3=match_result[match_result.format=='bo3']
match_result_BO5=match_result[match_result.format=='bo5']
match_result_BO1=match_result_BO1.reset_index(drop=True)

for i in range(len(match_result_BO1)):
    result1=(match_result_BO1['result'][i][:2]).strip()
    result2=(match_result_BO1['result'][i][-2:]).strip()
    match_result_BO1.at[i,'team1_result'] = int(result1)
    match_result_BO1.at[i,'team2_result'] = int(result2)
# %%
match_result_BO3=match_result_BO3.reset_index(drop=True)
match_result_BO5=match_result_BO5.reset_index(drop=True)
for i in range(len(match_result_BO3)):
    if match_result_BO3['team1_result'][i] > match_result_BO3['team2_result'][i]:
        win_team = match_result_BO3['team1'][i]
        lose_team = match_result_BO3['team2'][i]
    elif match_result_BO3['team2_result'][i] > match_result_BO3['team1_result'][i]:
        win_team = match_result_BO3['team2'][i]
        lose_team = match_result_BO3['team1'][i]
    match_result_BO3.at[i, 'W_id'] = win_team
    match_result_BO3.at[i, 'L_id'] = lose_team
for i in range(len(match_result_BO5)):
    if match_result_BO5['team1_result'][i] > match_result_BO5['team2_result'][i]:
        win_team = match_result_BO5['team1'][i]
        lose_team = match_result_BO5['team2'][i]
    elif match_result_BO5['team2_result'][i] > match_result_BO5['team1_result'][i]:
        win_team = match_result_BO5['team2'][i]
        lose_team = match_result_BO5['team1'][i]
    match_result_BO5.at[i, 'W_id'] = win_team
    match_result_BO5.at[i, 'L_id'] = lose_team
for i in range(len(match_result_BO1)):
    if match_result_BO1['team1_result'][i] > match_result_BO1['team2_result'][i]:
        win_team = match_result_BO1['team1'][i]
        lose_team = match_result_BO1['team2'][i]
    elif match_result_BO1['team2_result'][i] > match_result_BO1['team1_result'][i]:
        win_team = match_result_BO1['team2'][i]
        lose_team = match_result_BO1['team1'][i]
    match_result_BO1.at[i, 'W_id'] = win_team
    match_result_BO1.at[i, 'L_id'] = lose_team
#%%
match_result_total=pd.concat([match_result_BO1,match_result_BO3,match_result_BO5],axis=0)
# %%
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
#%%
match_result_total=match_result_total.sort_values(by='date',ascending='True')
match_result_total=match_result_total.reset_index(drop=True)
#%%
match_result_total_elo = team_id_match(match_result_total)
elo_team = elo_team.elo_team()
# %%
CSGO_ELO_match_result_total_score = elo_team.team_elo_constant_elo(match_result_total_elo)

CSGO_team_id = set(list(match_result_total_elo.W_id) + list(match_result_total_elo.L_id))
CSGO_team_id = pd.DataFrame(list(CSGO_team_id))

CSGO_team_id.index = CSGO_team_id[0]

CSGO_team_id['team_id'] = range(len(CSGO_team_id))

CSGO_team_id.rename(columns={0: 'Team_id'}, inplace=True)

CSGO_team_id['elo_score'] = CSGO_ELO_match_result_total_score

records1 = CSGO_team_id.to_dict('records')
match_db.CSGO_Team_elo.drop()
match_db.CSGO_Team_elo.insert_many(records1)
match_client.close()

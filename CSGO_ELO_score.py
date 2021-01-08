# %%
import pandas as pd
import pymongo
import DataBaseAccess_c as DBA
import elo
import elo_team
import imp
import re
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
match_client_data_source = pymongo.MongoClient('121.41.79.9', 7979)

# 连接database'damin'
match_db_data_source = match_client_data_source['crawler']
# 'admin'的账号密码
match_db_data_source.authenticate('yanziao', 'euOkM2gYuPdvxUbl')
# %%
# 获取比赛结果
CSGO_SHL_data = pd.DataFrame(list(
    match_db_data_source.csgo_match_result.find({}, {'team1_score': 1, 'team2_score': 1, 'event_name': 1, 'match.match_time': 1,
                                         'uuid': 1, 'bo': 1, 'data': 1})))

# %%
CSGO_SHL_data['data_info']= CSGO_SHL_data['data']
for i in range(len(CSGO_SHL_data)):
    if len(CSGO_SHL_data['data'][i]) > 0:
        data_info = CSGO_SHL_data['data'][i][0]
        CSGO_SHL_data.at[i, 'data_info'] = data_info
    else:
        CSGO_SHL_data=CSGO_SHL_data.drop(i)
CSGO_SHL_data = CSGO_SHL_data.reset_index(drop= True)
# %%
for i in range(len(CSGO_SHL_data)):
    team1_info = CSGO_SHL_data['data_info'][i]['team1']
    team2_info = CSGO_SHL_data['data_info'][i]['team2']
    team1_logo = team1_info['logo'] # 很多比赛的队伍id为0，所以会通过战队的logo重的ID来确认战队的id。
    team2_logo = team2_info['logo']
    team1_id = team1_info['id']
    team2_id = team2_info['id']
    if team1_id == 0:
        if len(team1_logo)>0:
            team1_id = re.findall('\d+',team1_logo)[0]
        else:
           pass
    else:
        team1_id = team1_id
    if team2_id == 0:
        if len(team2_logo) >0:
            team2_id = re.findall('\d+',team2_logo)[0]
        else:
            pass
    else:
        team2_id = team2_id
    event_name = CSGO_SHL_data['event_name'][i]
    match_date = CSGO_SHL_data['data_info'][i]['match']['match_time']
    CSGO_SHL_data.at[i, 'team1'] = team1_id
    CSGO_SHL_data.at[i, 'team2'] = team2_id
    CSGO_SHL_data['team1_result'] =CSGO_SHL_data['team1_score']
    CSGO_SHL_data['team2_result'] =CSGO_SHL_data['team2_score']
    CSGO_SHL_data.at[i, 'event_name'] = event_name
    CSGO_SHL_data.at[i,'date'] = match_date
match_result = CSGO_SHL_data.dropna()
match_result = CSGO_SHL_data.reset_index(drop=True)

# %%
match_result_BO1 = match_result[match_result.bo == 1]
match_result_BO3 = match_result[match_result.bo == 3]
match_result_BO5 = match_result[match_result.bo == 5]
match_result_BO1 = match_result_BO1.reset_index(drop=True)
#
# for i in range(len(match_result_BO1)):
#     result1 = (match_result_BO1['result'][i][:2]).strip()
#     result2 = (match_result_BO1['result'][i][-2:]).strip()
#     match_result_BO1.at[i, 'team1_result'] = int(result1)
#     match_result_BO1.at[i, 'team2_result'] = int(result2)
# %%
# match_result_BO1.to_csv('CSGO_BO1_result.csv')
# %%
match_result_BO3 = match_result_BO3.reset_index(drop=True)
match_result_BO5 = match_result_BO5.reset_index(drop=True)
for i in range(len(match_result_BO3)):
    if match_result_BO3['team1_result'][i] > match_result_BO3['team2_result'][i]:
        win_team = match_result_BO3['team1'][i]
        lose_team = match_result_BO3['team2'][i]
    elif match_result_BO3['team2_result'][i] > match_result_BO3['team1_result'][i]:
        win_team = match_result_BO3['team2'][i]
        lose_team = match_result_BO3['team1'][i]
    match_result_BO3.at[i, 'diff'] = abs(
        int(match_result_BO3['team1_result'][i]) - int(match_result_BO3['team2_result'][i]))
    match_result_BO3.at[i, 'W_id'] = win_team
    match_result_BO3.at[i, 'L_id'] = lose_team
for i in range(len(match_result_BO5)):
    if match_result_BO5['team1_result'][i] > match_result_BO5['team2_result'][i]:
        win_team = match_result_BO5['team1'][i]
        lose_team = match_result_BO5['team2'][i]
    elif match_result_BO5['team2_result'][i] > match_result_BO5['team1_result'][i]:
        win_team = match_result_BO5['team2'][i]
        lose_team = match_result_BO5['team1'][i]
    match_result_BO5.at[i, 'diff'] = abs(
        int(match_result_BO5['team1_result'][i]) - int(match_result_BO5['team2_result'][i]))
    match_result_BO5.at[i, 'W_id'] = win_team
    match_result_BO5.at[i, 'L_id'] = lose_team
for i in range(len(match_result_BO1)):
    if match_result_BO1['team1_result'][i] > match_result_BO1['team2_result'][i]:
        win_team = match_result_BO1['team1'][i]
        lose_team = match_result_BO1['team2'][i]
    elif match_result_BO1['team2_result'][i] > match_result_BO1['team1_result'][i]:
        win_team = match_result_BO1['team2'][i]
        lose_team = match_result_BO1['team1'][i]
    match_result_BO1.at[i, 'diff'] = 1
    match_result_BO1.at[i, 'W_id'] = win_team
    match_result_BO1.at[i, 'L_id'] = lose_team
# %%
match_result_total = pd.concat([match_result_BO1, match_result_BO3, match_result_BO5], axis=0)


# %%

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


# %%
match_result_total = match_result_total.sort_values(by='date', ascending='True')
# %%
# %%
match_result_total = match_result_total.dropna()
match_result_total = match_result_total.reset_index(drop=True)
# %%
match_result_total_elo = team_id_match(match_result_total)
# %%
elo_team = elo_team.elo_team()
# %%
CSGO_ELO_match_result_total_score, CSGO_ELO_team_played_count = elo_team.CSGO_team_elo_constant_elo(
    match_result_total_elo)

CSGO_team_id = set(list(match_result_total_elo.W_id) + list(match_result_total_elo.L_id))
CSGO_team_id = pd.DataFrame(list(CSGO_team_id))

CSGO_team_id.index = CSGO_team_id[0]

CSGO_team_id['team_id'] = range(len(CSGO_team_id))

CSGO_team_id.rename(columns={0: 'Team_id'}, inplace=True)

CSGO_team_id['elo_score'] = CSGO_ELO_match_result_total_score
CSGO_team_id['team_times'] = CSGO_ELO_team_played_count

records1 = CSGO_team_id.to_dict('records')
match_db.CSGO_Team_elo.drop()
match_db.CSGO_Team_elo.insert_many(records1)
match_client.close()
print('success update the CSGO ELO info')
#%%
match_result_total_elo.head()
# %%
for i in range(len(match_result_total_elo)):
    if match_result_total_elo['w_elo_before_game'][i]>match_result_total_elo['l_elo_before_game'][i]:
        match_result_total_elo.at[i,'result'] = 1
    elif match_result_total_elo['w_elo_before_game'][i]==match_result_total_elo['l_elo_before_game'][i]:
        match_result_total_elo.at[i,'result'] = 0.5
    else:
       match_result_total_elo.at[i,'result'] = 0 
# %%
import numpy as np
np.mean(match_result_total_elo['result'])
# %%

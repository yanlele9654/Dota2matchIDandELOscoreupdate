# -*- coding: UTF-8 -*-
#%%
import pandas as pd
import pymongo
import DataBaseAccess_c as DBA
import dota2_api


db_eng_1 = DBA.DbInfoGenerator('vpgame').info
# db_eng_2 = DBA.DbInfoGenerator('model_builder').info
# 连接到本地库
client = pymongo.MongoClient(db_eng_1['host'], 7974)
#    Newclient = pymongo.MongoClient(db_eng_2['host'], 27017)

# 连接database'damin'
db = client['admin']
# 'admin'的账号密码
db.authenticate(db_eng_1['user'], db_eng_1['password'])
print('success connet the database')
NewClient = pymongo.MongoClient('121.41.79.9',7979)
new_db = NewClient['crawler']
new_db.authenticate('yanziao','euOkM2gYuPdvxUbl')
print('success connet to the CSGO match database')

# 查询对应的比赛id并且建立list

dota_match = list(new_db.csgo_match_detail.find({}, {'_id': 0, 'third_id': 1,'team1':1,'team2':1}))
#%%
print(len(dota_match))
team1_player_info = []
for i in range(len(dota_match)):
    if 'team1' in dota_match[i].keys():
        #print('team1 in dota_match')
        if 'player_stat' in dota_match[i]['team1']:
            #print('player_stat in team1')
            for j in range(len(dota_match[i]['team1']['player_stat'])):
                    try:
                        player_info = dota_match[i]['team1']['player_stat'][j]
                    #print(player_info)
                        #player_info['match_id'] = dota_match[i]['third_id']
                    except KeyError:
                        continue
                    else:
                        player_info['match_id'] = dota_match[i]['third_id'] 
                        player_info['team_id'] = dota_match[i]['team1']['id']
                    #print(player_info)
                    #team1_player_info = team1_player_info.append(player_info)
                    #print(team1_player_info)
                    #team1_player_info = []
                        db.CSGO_players_info.insert_one(player_info)
    if 'team2' in dota_match[i].keys():
        if 'player_stat' in dota_match[i]['team2']:
            #print('player_stat in team1')
            for j in range(len(dota_match[i]['team2']['player_stat'])):
                    try:
                        player_info_2 = dota_match[i]['team2']['player_stat'][j]
                    #print(player_info)
                        #player_info['match_id'] = dota_match[i]['third_id']
                    except KeyError:
                        continue
                    else:
                        player_info_2['match_id'] = dota_match[i]['third_id'] 
                        player_info_2['team_id'] = dota_match[i]['team2']['id']
                    #print(player_info)
                    #team1_player_info = team1_player_info.append(player_info)
                    #print(team1_player_info)
                    #team1_player_info = []
                        db.CSGO_players_info.insert_one(player_info_2)
    print(i)
print('success insert data ready to calculate the elo')

# %%
dota_match[1085]['team1']['player_stat']
# %%

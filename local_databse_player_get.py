# %%
# -*- coding: UTF-8 -*-
import pandas as pd
import pymongo
from apscheduler.schedulers.blocking import BlockingScheduler

import DataBaseAccess_c as DBA
import dota2_api

db_eng_2 = DBA.DbInfoGenerator('model_builder').info
# 连接到本地库
Newclient = pymongo.MongoClient(db_eng_2['host'], 27017)
New_db = Newclient['admin']
# 'admin'的账号密码
New_db.authenticate(db_eng_2['user'], db_eng_2['password'])
print('success connet the model_builder database')
# 连接database'damin'
# 'admin'的账号密码
print('success connet the database')

# 查询对应的比赛id并且建立list

dota_match = list(New_db.match_data_2019_2020.find({}, {'_id': 0, 'match_id': 1,'start_time':1}))
#dota_match = pd.DataFrame(dota_match)
# 如果数据库内已经有数据，不插入这部分数据
player_info = list(New_db.player_info.find({}, {'_id': 0, 'match_id': 1}))
player_info = pd.DataFrame(player_info)
# 如果数据库内已经有数据，不插入这部分数据
match_list_haven = []
if len(player_info

       ) != 0:
    match_list_haven = list(player_info['match_id'])
# 对于以及在数据库的比赛进行筛选

#%%
m = 0
for mi in dota_match:

    if mi not in match_list_haven:
        data1 = list(New_db.match_data_2019_2020.find(
            {'match_id': mi['match_id']}, {'_id': 0, 'players': 1}))
        print('ready to insert match_id is %d' %(mi['match_id']))
        for i in range(len(data1)):
            if 'players' in data1[i].keys():
                for j in range(len(data1[i]['players'])):
                    player_info = data1[i]['players'][j]
                    New_db.players_2020.insert_one(player_info)
print('success insert data ready to calculate the elo')

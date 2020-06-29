import dota2_api
import pandas as pd
import pymongo

import DataBaseAccess_c as DBA

db_eng_1 = DBA.DbInfoGenerator('model_builder').info
client = pymongo.MongoClient(db_eng_1['host'], 27017)
# 连接database'damin'
db = client['admin']
# 'admin'的账号密码
db.authenticate(db_eng_1['user'], db_eng_1['password'])
#%%
list1 = range(4307203443, 4307213443, 1)
i=0
while i<4307213443:
    match_info = dota2_api.get_api_json(
        'https://api.opendota.com/api/matches/{}?ccdc7024-3890-44dd-b602-ec193dee6f23'.format(list1[i]))
    if len(match_info) <10:

        print('this match not found')
    else:
        db.Normal_matches_total_info.insert_one(match_info)
        i+=1
    print(i)
# print(list1[1])
#%%

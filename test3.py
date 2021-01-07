import pandas as pd
import pymongo
import time

import DataBaseAccess_c as DBA 

db_eng_1 = DBA.DbInfoGenerator('vpgame').info
client = pymongo.MongoClient(db_eng_1['host'], 7974)
# 连接database'damin'
db = client['admin']
# 'admin'的账号密码
db.authenticate(db_eng_1['user'], db_eng_1['password'])
print('success connet the database')

dota_players_2020 = pd.DataFrame(list(db.players_2020.find(
    {}, {"match_id": 1, "account_id": 1, "win": 1, '_id': 0, 'start_time': 1})))
dota_players_2020.to_csv('players_2020_info.csv')

dota_stats3 = pd.DataFrame(list(db.dota_basic_data_2020.find({}, {
    'radiant_team_id': 1, 'dire_team_id': 1, 'radiant_win': 1, 'match_id': 1, 'leagueid': 1, '_id': 0,
    'start_time': 1, 'league.tier': 1, 'duration': 1, 'series_id': 1})))
dota_stats3.to_csv('match_2020_info.csv')
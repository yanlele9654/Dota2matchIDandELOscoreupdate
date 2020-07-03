#%%
# -*- coding: UTF-8 -*-
import pandas as pd
import pymongo
import time
import DataBaseAccess_c as DBA
import dota2_api


def opentomongo():
    db_eng_2 = DBA.DbInfoGenerator('vpgame').info
    # 连接到本地库
    Newclient = pymongo.MongoClient(db_eng_2['host'], 7974)
    New_db = Newclient['admin']
    # 'admin'的账号密码
    New_db.authenticate(db_eng_2['user'], db_eng_2['password'])
    # 连接database'damin'
    # 'admin'的账号密码
    print('success connet the database')

    # sql语句建立查询
    sql = """
    SELECT
    matches.match_id,
    matches.start_time
    FROM matches
    JOIN match_patch using(match_id)
    WHERE TRUE
    AND matches.start_time between extract(epoch from timestamp '2020-01-01T00:00:00.000Z')
    and extract(epoch from timestamp '2021-01-01T00:00:00.000Z')
    """

    # 查询对应的比赛id并且建立list

    match_ids = dota2_api.get_api_json(
        'https://api.opendota.com/api/explorer?sql={}'.format(sql))['rows']

    print(len(match_ids))

    dota_match = list(New_db.dota_basic_data_2020.find({}, {'_id': 0, 'match_id': 1}))
    dota_match = pd.DataFrame(dota_match)
    # 如果数据库内已经有数据，不插入这部分数据
    match_list_haven = []
    if len(dota_match

           ) != 0:
        match_list_haven = list(dota_match['match_id'])
    # 查看还需要插入的比赛场次
    print(len(match_ids) - len(dota_match))

    # 对于以及在数据库的比赛进行筛选
    m = 0
    for mi in match_ids:
        # print(mi['match_id'])
        if mi['match_id'] not in match_list_haven:
            match_info = dota2_api.get_api_json(
                'https://api.opendota.com/api/matches/{}?ccdc7024-3890-44dd-b602-ec193dee6f23'.format(mi['match_id']))
            print(mi)
            New_db.dota_basic_data_2020.insert_one(match_info)
            m = m + 1
            print(m)
            # 将战队的历史数据中每个队员的历史数据插入到对应的数据库中
            data1 = list(New_db.dota_basic_data_2020.find(
                {'match_id': mi['match_id']}, {'_id': 0, 'players': 1}))
            print('ready to insert')
            for i in range(len(data1)):
                if 'players' in data1[i].keys():
                    for j in range(len(data1[i]['players'])):
                        player_info = data1[i]['players'][j]
                        New_db.players_2020.insert_one(player_info)
    print('success insert data ready to calculate the elo')

    # 关闭服务器
    # 关闭服务器


while True:
    opentomongo()
    time.sleep(2000)

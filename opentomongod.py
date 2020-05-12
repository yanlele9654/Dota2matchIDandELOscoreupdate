# -*- coding: UTF-8 -*-
import pandas as pd
import pymongo
from apscheduler.schedulers.blocking import BlockingScheduler

import DataBaseAccess_c as DBA
import dota2_api


def opentomongo():
    db_eng_1 = DBA.DbInfoGenerator('vpgame').info

    # 连接到本地库
    client = pymongo.MongoClient("dds-bp1f5b9c442b9524-pub.mongodb.rds.aliyuncs.com", 3717)

    # 连接database'damin'
    db = client['admin']
    # 'admin'的账号密码
    db.authenticate(db_eng_1['user'], db_eng_1['password'])

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

    dota_match = list(db.dota_basic_data_2020.find({}, {'_id': 0, 'match_id': 1}))
    dota_match = pd.DataFrame(dota_match)
    # 如果数据库内已经有数据，不插入这部分数据
    match_list_haven = []
    if len(dota_match

           ) != 0:
        match_list_haven = list(dota_match['match_id'])
    # 查看还需要插入的比赛场次
    print(len(match_ids) - len(dota_match) + 1)

    # 对于以及在数据库的比赛进行筛选
    m = 0
    for mi in match_ids:
        # print(mi['match_id'])
        if mi['match_id'] not in match_list_haven:
            match_info = dota2_api.get_api_json(
                'https://api.opendota.com/api/matches/{}'.format(mi['match_id']))
            print(mi)
            db.dota_basic_data_2020.insert_one(match_info)
            m = m + 1
            print(m)
            # 将战队的历史数据中每个队员的历史数据插入到对应的数据库中
            data1 = list(db.dota_basic_data_2020.find(
                {'match_id': mi['match_id']}, {'_id': 0, 'players': 1}))
            print('ready to insert')
            for i in range(len(data1)):
                if 'players' in data1[i].keys():
                    for j in range(len(data1[i]['players'])):
                        player_info = data1[i]['players'][j]
                        db.players_2020.insert_one(player_info)
    print('success insert data ready to calculate the elo')

    # 关闭服务器
    # 关闭服务器

    # client.close()
    dota_players_2019 = pd.DataFrame(list(db.players_2019.find(
        {}, {"match_id": 1, "account_id": 1, "win": 1, '_id': 0, 'start_time': 1})))
    dota_players_2018 = pd.DataFrame(list(db.players_2018.find(
        {}, {"match_id": 1, "account_id": 1, "win": 1, '_id': 0, 'start_time': 1})))
    dota_players_2020 = pd.DataFrame(list(db.players_2020.find(
        {}, {"match_id": 1, "account_id": 1, "win": 1, '_id': 0, 'start_time': 1})))
    dota_players_2019 = dota_players_2019.append(dota_players_2020)
    dota_players_2019 = dota_players_2019.append(dota_players_2018)
    dota_players_2019 = dota_players_2019.sort_values(by=['start_time', 'match_id'])
    dota_players_2019 = dota_players_2019.reset_index(drop=True)
    dota_players_2019_win = dota_players_2019[dota_players_2019.win == 1]
    dota_players_2019_win = dota_players_2019_win.reset_index(drop=True)
    W_id = []
    W_account = []
    for i in range(len(dota_players_2019_win) - 1):
        if dota_players_2019_win.match_id[i] == dota_players_2019_win.match_id[i + 1]:
            W_id.append(dota_players_2019_win.account_id[i])
        else:
            W_id.append(dota_players_2019_win.account_id[i])
            W_account.append(W_id)
            W_id = []
    dota_players_2019_lose = dota_players_2019[dota_players_2019.win == 0]

    dota_players_2019_lose = dota_players_2019_lose.reset_index(drop=True)
    L_id = []
    L_account = []
    for i in range(len(dota_players_2019_lose) - 1):
        if dota_players_2019_lose.match_id[i] == dota_players_2019_lose.match_id[i + 1]:
            L_id.append(dota_players_2019_lose.account_id[i])
        else:
            L_id.append(dota_players_2019_lose.account_id[i])
            L_account.append(L_id)
            L_id = []

    match_id = dota_players_2019_win.groupby('match_id')['match_id'].head(1)
    match_id = match_id.reset_index(drop=True)
    match_id = match_id.drop(match_id.index[-1])
    match_id = list(match_id)
    start_time = dota_players_2019_win.groupby('match_id')['start_time'].head(1)
    start_time = start_time.reset_index(drop=True)
    start_time = start_time.drop(start_time.index[-1])
    #start_time = list(start_time)
    Winer_players = pd.DataFrame([match_id, W_account, L_account])
    Winer_players = Winer_players.T
    Winer_players.columns = ['match_id', 'W_account', 'L_account']

    dota_stats = list(db.dota_basic_data_2019.find({}, {
        'radiant_team.team_id': 1, 'dire_team.team_id': 1, 'radiant_win': 1, 'match_id': 1, 'leagueid': 1, '_id': 0,
        'start_time': 1, 'league.tier': 1, 'duration': 1, 'series_id': 1}))
    dota_stats_old = list(db.dota_basic_data_2018.find({}, {
        'radiant_team.team_id': 1, 'dire_team.team_id': 1, 'radiant_win': 1, 'match_id': 1, 'leagueid': 1, '_id': 0,
        'start_time': 1, 'league.tier': 1, 'duration': 1, 'series_id': 1}))
    dota_stats_new = list(db.dota_basic_data_2020.find({}, {
        'radiant_team.team_id': 1, 'dire_team.team_id': 1, 'radiant_win': 1, 'match_id': 1, 'leagueid': 1, '_id': 0,
        'start_time': 1, 'league.tier': 1, 'duration': 1, 'series_id': 1}))
    print('success get the match info')
    dota_stats1 = pd.DataFrame(dota_stats)
    dota_stats2 = pd.DataFrame(dota_stats_old)
    dota_stats3 = pd.DataFrame(dota_stats_new)
    dota_stats1 = dota_stats1.append(dota_stats3)
    dota_stats1 = dota_stats1.append(dota_stats2)
    dota_stats1 = dota_stats1.dropna(axis=0, how='any')
    dota_stats1 = dota_stats1.reset_index()
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
    dota_stats1 = dota_stats1.dropna(subset=['duration', 'dire_team', 'radiant_team'])
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
        dire_team_id.append(str(row.dire_team['team_id']))
        radiant_team_id.append(str(row.radiant_team['team_id']))
    dota_stats1['dire_team'] = dire_team_id
    dota_stats1['radiant_team'] = radiant_team_id

    ## ELO评分team
    dota_stats1 = dota_stats1.reset_index(drop=True)
    W_id = []
    L_id = []
    League_tier = []
    for i in range(len(dota_stats1)):
        League_tier.append(dota_stats1['league'][i]['tier'])
        if dota_stats1['radiant_win'][i] == 0:
            W_id.append(int(dota_stats1['dire_team'][i]))
            L_id.append(int(dota_stats1['radiant_team'][i]))
        else:
            W_id.append(int(dota_stats1['radiant_team'][i]))
            L_id.append(int(dota_stats1['dire_team'][i]))
    dota_stats1['W_id'] = W_id
    dota_stats1['L_id'] = L_id
    dota_stats1['tier'] = League_tier

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

    dota_stats1 = team_id_match(dota_stats1)

    import elo_player as elo_player

    elo_player = elo_player.elo_player()

    dota_stats1_elo = elo_player.player_team_elo_result(dota_stats1, total_players_id, 16)

    dota_team_id = set(list(dota_stats1.W_id) + list(dota_stats1.L_id))
    dota_team_id = pd.DataFrame(list(dota_team_id))

    dota_team_id.index = dota_team_id[0]

    dota_team_id['team_id'] = range(len(dota_team_id))

    dota_team_id.rename(columns={0: 'Team_id'}, inplace=True)

    dota_team_id['elo_score'] = dota_stats1_elo

    records1 = dota_team_id.to_dict('records')

    db.player_Team_elo.drop()
    db.player_Team_elo.insert_many(records1)
    print('success insert the new Elo score')
    client.close()


#def dojob():
#   scheduler = BlockingScheduler()
#   scheduler.add_job(opentomongo, 'interval', seconds=600, id='insertData&CalculateElo')
#   scheduler.start()


#dojob()


opentomongo()

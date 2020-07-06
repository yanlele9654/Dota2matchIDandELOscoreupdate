import threading
import dota2_api
import pandas as pd
import pymongo
import _thread
import DataBaseAccess_c as DBA

db_eng_1 = DBA.DbInfoGenerator('model_builder').info
client = pymongo.MongoClient(db_eng_1['host'], 27017)
# 连接database'damin'
db = client['admin']
# 'admin'的账号密码
db.authenticate(db_eng_1['user'], db_eng_1['password'])


# %%
def normal_match_insert(ids):
    for i in ids:
        match_info = dota2_api.get_api_json(
            'https://api.opendota.com/api/matches/{}?ccdc7024-3890-44dd-b602-ec193dee6f23'.format(i))
        if len(match_info) < 10:
        # i+=1
            print("当前线程：", threading.currentThread().name, "----", i, 'this match not found')
        else:
            db.Normal_matches_total_info.insert_one(match_info)
        # i+=1
            print("当前线程：", threading.currentThread().name, "----", 'success insert match_id', i)


def thread_num(Start_match_id,End_match_id, num):  # 传参是打印数字的总数及线程数
    total=End_match_id-Start_match_id
    data = [x for x in range(Start_match_id, End_match_id)]  # 所有的数字循环放入list
    split_data = [data[i: i + int(total / num)] for i in
                  range(0, len(data), int(total / num))]  # 带步长的循环list，且每段放入一个list，生成2维数组
    print(len(split_data))
    for d in split_data:  # 循环二维数组，每次取一个数组，作为打印函数的传参
        t = threading.Thread(target=normal_match_insert, args=(d,))  # 生成线程且调用方法及给予传参
        t = t.start()  # 启动线程

    while threading.active_count() != 1:  # 等待子线程
        pass


thread_num(1000000, 100)  # 调用线程方法
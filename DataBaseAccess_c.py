import os

db_name_link = {'renren': [1, 1], 'admin': [0, 0], 'shuju': [2, 2], 'vpgame': [3, 3], 'model_builder': [4, 4]}

db_SSH_info = [
    {'host': '47.110.60.36',
     'user': 'root',
     'password': 'Xigua%@$',
     'remote_bind_address': 'dds-bp149495a87e75d41.mongodb.rds.aliyuncs.com'},
    # MongoDB
    {'host': '47.110.60.36',
     'user': 'root',
     'password': 'Xigua%@$',
     'remote_bind_address': 'rm-6web1qzk40v57h14lio.mysql.japan.rds.aliyuncs.com',
     },

    # 西瓜下注单 SQL
    {'host': '47.110.60.36',
     'user': 'root',
     'password': 'Xigua%@$',
     'remote_bind_address': 'rm-bp190sddgeyjm1n21.mysql.rds.aliyuncs.com',
     },
    # SQL数据库
    {'host': 'dds-bp1f5b9c442b9524-pub.mongodb.rds.aliyuncs.com',
     'user': 'root',
     'password': 'VPGame%2019Hz',
     # 'remote_bind_address': 'dds-bp1f5b9c442b9524-pub.mongodb.rds.aliyuncs.com'
     },
    # Vpgame 数据库
]

db_link_info = [
    {'user': 'yanziao',
     'password': 'yanziao',
     'host': '127.0.0.1'},
    # MongoDB
    {'user': 'testtn',
     'password': '!QAZxsw2',
     'host': '127.0.0.1'
     },
    # 西瓜下注单
    {'user': 'yanziao',
     'password': 'yanziaoaA!',
     'host': '127.0.0.1'
     },
    {'user': 'root',
     'password': 'VPGame%2019Hz',
     'host': 'dds-bp1f5b9c442b9524-pub.mongodb.rds.aliyuncs.com'
     },
    {'user':'model_builder',
     'password':'vpgame2020',
     'host':'172.16.3.52'}
]

db_json_file_path = os.getcwd()


class DbInfoGenerator:
    def __init__(self, database_name):
        self.info = db_link_info[db_name_link[database_name][1]].copy()
        self.info['database'] = database_name


class DbSSHGenerator:
    def __init__(self, database_name):
        self.info = db_SSH_info[db_name_link[database_name][0]].copy()
        self.info['database'] = database_name

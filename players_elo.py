#%%
import pymongo
import pandas as pd 
import DataBaseAccess_c as DBA

db_eng_1 = DBA.DbInfoGenerator('vpgame').info
client = pymongo.MongoClient(db_eng_1['host'], 7974)
# 连接database'damin'
db = client['admin']
# 'admin'的账号密码
db.authenticate(db_eng_1['user'], db_eng_1['password'])
print('success connet the database')
#%%
player_elo_info = pd.DataFrame(list(db.dota2_players_elo.find({},{'_id':0, 'account_id':1 , 'elo_score':1 } )))

team_elo_info = pd.DataFrame(list(db.player_Team_elo.find({},{'_id':0,
'Team_id':1 , 'elo_score':1, 'played_times':1})))
#%%
team_elo_info = team_elo_info[team_elo_info['played_times']>10]
# %%
import matplotlib.pyplot as plt
# %%
plt.hist(player_elo_info['elo_score'], bins=100, rwidth=0.8, density=True)
#%%
plt.hist(player_elo_info['elo_score'], bins=100, rwidth=0.8, density=True)

# %%
from scipy import stats
mean =player_elo_info['elo_score'].mean()
std = player_elo_info['elo_score'].std()
stats.kstest(player_elo_info['elo_score'], 'norm', (mean, std))
# %%
k2, p = stats.normaltest(team_elo_info['elo_score'])
alpha = 1e-10
if p < alpha: # null hypothesis: x comes from a normal distribution
  print("The null hypothesis can be rejected") # 原假设可被拒绝,即不是正态分布
else:
  print("The null hypothesis cannot be rejected") # 原假设不可被拒绝,即使正态分布

# %%
print(p)
# %%

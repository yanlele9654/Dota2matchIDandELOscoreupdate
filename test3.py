# %%
import pandas as pd
import pymongo
import time

import DataBaseAccess_c as DBA 
data = pd.read_csv('Dota_ELO_info_player_0104.csv ')

# %%
import numpy as np
np.mean(data['result_team'])
# %%
np.mean(data['result_player'])
# %%

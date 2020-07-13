import numpy as np
import pandas as pd
import itertools
import elo as elo

elo=elo.elo()
class elo_team:
    def __init__(self):
        self.k_factor=16
        
    def team_elo_recent(self,Major_chongqing_major_Elo,k_score_recent1=16, k_score_recent2=32):
        dota_team_id=set(list(Major_chongqing_major_Elo.W_id)+list(Major_chongqing_major_Elo.L_id))
        n_teams = len(dota_team_id)
        mean_elo=1000
        current_elos = np.ones(shape=(n_teams))*mean_elo
        current_count = np.zeros(n_teams)
        last_start_time = np.zeros(shape=n_teams)
        last_win_before = np.zeros(shape=(n_teams))
        for row in Major_chongqing_major_Elo.itertuples():
            idx = row.Index
            w_id = row.W_team_id
            l_id = row.L_team_id
            start_time = row.start_time
            current_time = row.current_time
            recent_game =1 if start_time > (current_time - 5270400) else 0
            # print(type(w_id))
            # Get current elos
            w_elo_before = current_elos[w_id]
            l_elo_before = current_elos[l_id]
            w_team_times = current_count[w_id]
            l_team_times = current_count[l_id]
            w_team_last_start_time = last_start_time[w_id]
            l_team_last_start_time = last_start_time[l_id]
            # Update on game results
            w_elo_after, l_elo_after = elo.update_elo_recent(w_elo_before, l_elo_before, recent_game, k_score_recent1, k_score_recent2)
            w_team_times, l_team_times = w_team_times+1 ,l_team_times+1   # 计算出战队到最新打了多少次比赛
            w_team_last_start_time, l_team_last_start_time = start_time, start_time
            w_team_current, l_team_current = 1, 0
            # Save updated elos
            Major_chongqing_major_Elo.at[idx, 'w_elo_before_game'] = w_elo_before
            Major_chongqing_major_Elo.at[idx, 'l_elo_before_game'] = l_elo_before
            Major_chongqing_major_Elo.at[idx, 'w_elo_after_game'] = w_elo_after
            Major_chongqing_major_Elo.at[idx, 'l_elo_after_game'] = l_elo_after
            Major_chongqing_major_Elo.at[idx, 'w_team_times'] = w_team_times
            Major_chongqing_major_Elo.at[idx, 'l_team_times'] = l_team_times
            Major_chongqing_major_Elo.at[idx, 'w_team_last_start_time'] = last_start_time[w_id]
            Major_chongqing_major_Elo.at[idx, 'l_team_last_start_time'] = last_start_time[l_id]
            Major_chongqing_major_Elo.at[idx, 'w_team_before'] = last_win_before[w_id]
            Major_chongqing_major_Elo.at[idx, 'l_team_before'] = last_win_before[l_id]
            
            current_elos[w_id] = w_elo_after
            current_elos[l_id] = l_elo_after
            current_count[w_id] = w_team_times
            current_count[l_id] = l_team_times
            last_start_time[w_id] = w_team_last_start_time
            last_start_time[l_id] = l_team_last_start_time
            last_win_before[w_id] = w_team_current
            last_win_before[l_id] = l_team_current

        Major_chongqing_major_Elo['win_team_elo']=Major_chongqing_major_Elo.w_elo_before_game
        Major_chongqing_major_Elo['Lose_team_elo']=Major_chongqing_major_Elo.l_elo_before_game
        Major_chongqing_major_Elo['dire_team_id']= Major_chongqing_major_Elo.dire_team
        Major_chongqing_major_Elo['radiant_team_id'] = Major_chongqing_major_Elo.radiant_team
        ## win_percent
        expected_list = []
        for row in Major_chongqing_major_Elo.itertuples():
            w_elo = row.w_elo_before_game
            l_elo = row.l_elo_before_game
            w_expected = elo.expected_result(w_elo, l_elo)
            expected_list.append(w_expected)
        Major_chongqing_major_Elo['win_predict'] = expected_list
        Major_chongqing_major_Elo['lose_predict'] = 1-Major_chongqing_major_Elo.win_predict
        result=[]
        for row in Major_chongqing_major_Elo.itertuples():
            if row.win_predict>0.5:
                result.append(1)
            else:
                result.append(0)
        Major_chongqing_major_Elo['result']=result
        return(Major_chongqing_major_Elo)
   
    def team_elo_constant(self,Major_chongqing_major_Elo, k_score =16):
        dota_team_id=set(list(Major_chongqing_major_Elo.W_id)+list(Major_chongqing_major_Elo.L_id))
        n_teams = len(dota_team_id)
        mean_elo=1000
        current_elos = np.ones(shape=(n_teams))*mean_elo
        for row in Major_chongqing_major_Elo.itertuples():
            idx = row.Index
            w_id = row.W_team_id
            l_id = row.L_team_id
            # Get current elos
            w_elo_before = current_elos[w_id]
            l_elo_before = current_elos[l_id]
            # Update on game results
            w_elo_after, l_elo_after = elo.update_elo_constant_k(w_elo_before, l_elo_before, k_score)
            # Save updated elos
            Major_chongqing_major_Elo.at[idx, 'w_elo_before_game'] = w_elo_before
            Major_chongqing_major_Elo.at[idx, 'l_elo_before_game'] = l_elo_before
            Major_chongqing_major_Elo.at[idx, 'w_elo_after_game'] = w_elo_after
            Major_chongqing_major_Elo.at[idx, 'l_elo_after_game'] = l_elo_after
            current_elos[w_id] = w_elo_after
            current_elos[l_id] = l_elo_after

        Major_chongqing_major_Elo['win_team_elo']=Major_chongqing_major_Elo.w_elo_before_game
        Major_chongqing_major_Elo['Lose_team_elo']=Major_chongqing_major_Elo.l_elo_before_game
#        Major_chongqing_major_Elo['dire_team_id']= Major_chongqing_major_Elo.dire_team
#        Major_chongqing_major_Elo['radiant_team_id'] = Major_chongqing_major_Elo.radiant_team
        ## win_percent
        expected_list = []
        for row in Major_chongqing_major_Elo.itertuples():
            w_elo = row.w_elo_before_game
            l_elo = row.l_elo_before_game
            w_expected = elo.expected_result(w_elo, l_elo)
            expected_list.append(w_expected)
        Major_chongqing_major_Elo['win_predict'] = expected_list
        Major_chongqing_major_Elo['lose_predict'] = 1-Major_chongqing_major_Elo.win_predict
        result=[]
        for row in Major_chongqing_major_Elo.itertuples():
            if row.win_predict>0.5:
                result.append(1)
            else:
                result.append(0)
        Major_chongqing_major_Elo['result']=result
        return(Major_chongqing_major_Elo)
    
    def team_elo_last(self,Major_chongqing_major_Elo, k_score_last=16, k_score_last2=32):
        dota_team_id=set(list(Major_chongqing_major_Elo.W_id)+list(Major_chongqing_major_Elo.L_id))
        n_teams = len(dota_team_id)
        mean_elo=1000
        current_elos = np.ones(shape=(n_teams))*mean_elo
        current_count = np.zeros(n_teams)
        last_start_time = np.zeros(shape=n_teams)
        last_win_before = np.zeros(shape=(n_teams))
        for row in Major_chongqing_major_Elo.itertuples():
            idx = row.Index
            w_id = row.W_team_id
            l_id = row.L_team_id
            start_time = row.start_time
            # print(type(w_id))
            # Get current elos
            w_elo_before = current_elos[w_id]
            l_elo_before = current_elos[l_id]
            w_team_times = current_count[w_id]
            l_team_times = current_count[l_id]
            w_team_last_start_time = last_start_time[w_id]
            l_team_last_start_time = last_start_time[l_id]
            w_team_last_start_time, l_team_last_start_time = start_time, start_time
            w_team_current, l_team_current = 1, 0       
            w_team_last = last_win_before[w_id]
            l_team_last = last_win_before[l_id]
            # Update on game results
            w_elo_after, l_elo_after = elo.update_elo_last(w_elo_before, l_elo_before, w_team_last, l_team_last,k_score_last, k_score_last2)
            w_team_times, l_team_times = w_team_times+1 ,l_team_times+1   # 计算出战队到最新打了多少次比赛

            # Save updated elos
            Major_chongqing_major_Elo.at[idx, 'w_elo_before_game'] = w_elo_before
            Major_chongqing_major_Elo.at[idx, 'l_elo_before_game'] = l_elo_before
            Major_chongqing_major_Elo.at[idx, 'w_elo_after_game'] = w_elo_after
            Major_chongqing_major_Elo.at[idx, 'l_elo_after_game'] = l_elo_after
            Major_chongqing_major_Elo.at[idx, 'w_team_times'] = w_team_times
            Major_chongqing_major_Elo.at[idx, 'l_team_times'] = l_team_times
            Major_chongqing_major_Elo.at[idx, 'w_team_last_start_time'] = last_start_time[w_id]
            Major_chongqing_major_Elo.at[idx, 'l_team_last_start_time'] = last_start_time[l_id]
            Major_chongqing_major_Elo.at[idx, 'w_team_before'] = last_win_before[w_id]
            Major_chongqing_major_Elo.at[idx, 'l_team_before'] = last_win_before[l_id]
            current_elos[w_id] = w_elo_after
            current_elos[l_id] = l_elo_after
            current_count[w_id] = w_team_times
            current_count[l_id] = l_team_times
            last_start_time[w_id] = w_team_last_start_time
            last_start_time[l_id] = l_team_last_start_time
            last_win_before[w_id] = w_team_current
            last_win_before[l_id] = l_team_current

        Major_chongqing_major_Elo['win_team_elo']=Major_chongqing_major_Elo.w_elo_before_game
        Major_chongqing_major_Elo['Lose_team_elo']=Major_chongqing_major_Elo.l_elo_before_game
        Major_chongqing_major_Elo['dire_team_id']= Major_chongqing_major_Elo.dire_team
        Major_chongqing_major_Elo['radiant_team_id'] = Major_chongqing_major_Elo.radiant_team
        ## win_percent
        expected_list = []
        for row in Major_chongqing_major_Elo.itertuples():
            w_elo = row.w_elo_before_game
            l_elo = row.l_elo_before_game
            w_expected = elo.expected_result( w_elo, l_elo)
            expected_list.append(w_expected)
        Major_chongqing_major_Elo['win_predict'] = expected_list
        Major_chongqing_major_Elo['lose_predict'] = 1-Major_chongqing_major_Elo.win_predict
        result=[]
        for row in Major_chongqing_major_Elo.itertuples():
            if row.win_predict>0.5:
                result.append(1)
            else:
                result.append(0)
        Major_chongqing_major_Elo['result']=result
        return(Major_chongqing_major_Elo)
        
    def team_elo_team_score(self,Major_chongqing_major_Elo,k_score_higher=16,k_score_lower=32,elo_score_standard=1100):
        dota_team_id=set(list(Major_chongqing_major_Elo.W_id)+list(Major_chongqing_major_Elo.L_id))
        n_teams = len(dota_team_id)
        mean_elo=1000
        current_elos = np.ones(shape=(n_teams))*mean_elo
        current_count = np.zeros(n_teams)
        last_start_time = np.zeros(shape=n_teams)
        last_win_before = np.zeros(shape=(n_teams))
        for row in Major_chongqing_major_Elo.itertuples():
            idx = row.Index
            w_id = row.W_team_id
            l_id = row.L_team_id
            start_time = row.start_time
            #current_time = row.current_time
            #recent_game =1 if start_time > (current_time - 5270400) else 0
            # print(type(w_id))
            # Get current elos
            w_elo_before = current_elos[w_id]
            l_elo_before = current_elos[l_id]
            w_team_times = current_count[w_id]
            l_team_times = current_count[l_id]
            w_team_last_start_time = last_start_time[w_id]
            l_team_last_start_time = last_start_time[l_id]
            # Update on game results
            w_elo_after, l_elo_after = elo.update_elo_team_score(w_elo_before, l_elo_before, k_score_higher, k_score_lower)
            w_team_times, l_team_times = w_team_times+1 ,l_team_times+1   # 计算出战队到最新打了多少次比赛
            w_team_last_start_time, l_team_last_start_time = start_time, start_time
            w_team_current, l_team_current = 1, 0
            # Save updated elos
            Major_chongqing_major_Elo.at[idx, 'w_elo_before_game'] = w_elo_before
            Major_chongqing_major_Elo.at[idx, 'l_elo_before_game'] = l_elo_before
            Major_chongqing_major_Elo.at[idx, 'w_elo_after_game'] = w_elo_after
            Major_chongqing_major_Elo.at[idx, 'l_elo_after_game'] = l_elo_after
            Major_chongqing_major_Elo.at[idx, 'w_team_times'] = w_team_times
            Major_chongqing_major_Elo.at[idx, 'l_team_times'] = l_team_times
            Major_chongqing_major_Elo.at[idx, 'w_team_last_start_time'] = last_start_time[w_id]
            Major_chongqing_major_Elo.at[idx, 'l_team_last_start_time'] = last_start_time[l_id]
            Major_chongqing_major_Elo.at[idx, 'w_team_before'] = last_win_before[w_id]
            Major_chongqing_major_Elo.at[idx, 'l_team_before'] = last_win_before[l_id]
            current_elos[w_id] = w_elo_after
            current_elos[l_id] = l_elo_after
            current_count[w_id] = w_team_times
            current_count[l_id] = l_team_times
            last_start_time[w_id] = w_team_last_start_time
            last_start_time[l_id] = l_team_last_start_time
            last_win_before[w_id] = w_team_current
            last_win_before[l_id] = l_team_current

        Major_chongqing_major_Elo['win_team_elo']=Major_chongqing_major_Elo.w_elo_before_game
        Major_chongqing_major_Elo['Lose_team_elo']=Major_chongqing_major_Elo.l_elo_before_game
        Major_chongqing_major_Elo['dire_team_id']= Major_chongqing_major_Elo.dire_team
        Major_chongqing_major_Elo['radiant_team_id'] = Major_chongqing_major_Elo.radiant_team
        ## win_percent
        expected_list = []
        for row in Major_chongqing_major_Elo.itertuples():
            w_elo = row.w_elo_before_game
            l_elo = row.l_elo_before_game
            w_expected = elo.expected_result(w_elo, l_elo)
            expected_list.append(w_expected)
        Major_chongqing_major_Elo['win_predict'] = expected_list
        Major_chongqing_major_Elo['lose_predict'] = 1-Major_chongqing_major_Elo.win_predict
        result=[]
        for row in Major_chongqing_major_Elo.itertuples():
            if row.win_predict>0.5:
                result.append(1)
            else:
                result.append(0)
        Major_chongqing_major_Elo['result']=result
        return(Major_chongqing_major_Elo)
    
        
    
    def team_elo_constant_elo(self,Major_chongqing_major_Elo, k_score =16):
        dota_team_id=set(list(Major_chongqing_major_Elo.W_id)+list(Major_chongqing_major_Elo.L_id))
        n_teams = len(dota_team_id)
        mean_elo=1000
        current_elos = np.ones(shape=(n_teams))*mean_elo
        current_count = np.zeros(n_teams)
        last_start_time = np.zeros(shape=n_teams)
        last_win_before = np.zeros(shape=(n_teams))
        for row in Major_chongqing_major_Elo.itertuples():
            idx = row.Index
            w_id = row.W_team_id
            l_id = row.L_team_id
            start_time = row.date
            w_elo_before = current_elos[w_id]
            l_elo_before = current_elos[l_id]
            w_team_times = current_count[w_id]
            l_team_times = current_count[l_id]
            w_team_last_start_time = last_start_time[w_id]
            l_team_last_start_time = last_start_time[l_id]
            # Update on game results
            w_elo_after, l_elo_after = elo.update_elo_constant_k(w_elo_before, l_elo_before, k_score)
            w_team_times, l_team_times = w_team_times+1 ,l_team_times+1   # 计算出战队到最新打了多少次比赛
            w_team_last_start_time, l_team_last_start_time = start_time, start_time
            w_team_current, l_team_current = 1, 0
            # Save updated elos
            Major_chongqing_major_Elo.at[idx, 'w_elo_before_game'] = w_elo_before
            Major_chongqing_major_Elo.at[idx, 'l_elo_before_game'] = l_elo_before
            Major_chongqing_major_Elo.at[idx, 'w_elo_after_game'] = w_elo_after
            Major_chongqing_major_Elo.at[idx, 'l_elo_after_game'] = l_elo_after
            Major_chongqing_major_Elo.at[idx, 'w_team_times'] = w_team_times
            Major_chongqing_major_Elo.at[idx, 'l_team_times'] = l_team_times
            Major_chongqing_major_Elo.at[idx, 'w_team_last_start_time'] = last_start_time[w_id]
            Major_chongqing_major_Elo.at[idx, 'l_team_last_start_time'] = last_start_time[l_id]
            Major_chongqing_major_Elo.at[idx, 'w_team_before'] = last_win_before[w_id]
            Major_chongqing_major_Elo.at[idx, 'l_team_before'] = last_win_before[l_id]
            current_elos[w_id] = w_elo_after
            current_elos[l_id] = l_elo_after
            current_count[w_id] = w_team_times
            current_count[l_id] = l_team_times
            last_start_time[w_id] = w_team_last_start_time
            last_start_time[l_id] = l_team_last_start_time
            last_win_before[w_id] = w_team_current
            last_win_before[l_id] = l_team_current


        return(current_elos)
    
    
    def team_elo_last_elo(self,Major_chongqing_major_Elo, k_score_last=16, k_score_last2=32):
        dota_team_id=set(list(Major_chongqing_major_Elo.W_id)+list(Major_chongqing_major_Elo.L_id))
        n_teams = len(dota_team_id)
        mean_elo=1000
        current_elos = np.ones(shape=(n_teams))*mean_elo
        current_count = np.zeros(n_teams)
        last_start_time = np.zeros(shape=n_teams)
        last_win_before = np.zeros(shape=(n_teams))
        for row in Major_chongqing_major_Elo.itertuples():
            w_id = row.W_team_id
            l_id = row.L_team_id
            start_time = row.start_time
            #current_time = row.current_time
            #lairecent_game =1 if start_time > (current_time - 5270400) else 0
            # Get current elos
            w_elo_before = current_elos[w_id]
            l_elo_before = current_elos[l_id]
            w_team_times = current_count[w_id]
            l_team_times = current_count[l_id]
            w_team_last_start_time = last_start_time[w_id]
            l_team_last_start_time = last_start_time[l_id]
            w_team_last_start_time, l_team_last_start_time = start_time, start_time
            w_team_current, l_team_current = 1, 0       
            w_team_last = last_win_before[w_id]
            l_team_last = last_win_before[l_id]
            # Update on game results
            w_elo_after, l_elo_after = elo.update_elo_last(w_elo_before, l_elo_before, w_team_last, l_team_last,k_score_last, k_score_last2)
            w_team_times, l_team_times = w_team_times+1 ,l_team_times+1   # 计算出战队到最新打了多少次比赛

            # Save updated elos

            current_elos[w_id] = w_elo_after
            current_elos[l_id] = l_elo_after
            current_count[w_id] = w_team_times
            current_count[l_id] = l_team_times
            last_start_time[w_id] = w_team_last_start_time
            last_start_time[l_id] = l_team_last_start_time
            last_win_before[w_id] = w_team_current
            last_win_before[l_id] = l_team_current


        return(current_elos)
    
    
    def player_team_elo_constant(self, data_total_info,total_players_id,k_factor=16):
        dota_team_id=set(list(data_total_info.W_id)+list(data_total_info.L_id))
        dota_team_id=pd.DataFrame(list(dota_team_id))
        dota_team_id.index=dota_team_id[0]
        dota_team_id['team_id']=range(len(dota_team_id))
        
        W_team_id=[]
        L_team_id=[]
        mean_elo=1000.0
        n_players = len(total_players_id)
        n_teams = len(dota_team_id)
        current_elos_player = np.ones(shape=(n_players))*mean_elo
        current_elos_team = np.ones(shape=(n_teams))*mean_elo
        current_count = np.zeros(n_teams)

        for i in range(len(data_total_info)):
            W_team_id.append(dota_team_id['team_id'][data_total_info['W_id'][i]])
            L_team_id.append(dota_team_id['team_id'][data_total_info['L_id'][i]])
        data_total_info['W_team_id']=W_team_id
        data_total_info['L_team_id']=L_team_id
        for row in data_total_info.itertuples():

            idx = row.Index

            # player elo 
            w_account1=row.W_players_1
            l_account1=row.L_players_1

            w_account2=row.W_players_2
            l_account2=row.L_players_2

            w_account3=row.W_players_3
            l_account3=row.L_players_3

            w_account4=row.W_players_4
            l_account4=row.L_players_4

            w_account5=row.W_players_5
            l_account5=row.L_players_5



            # tier = row.tier
            # print(type(w_id))
            # Get current elos
            w_elo_before1 = current_elos_player[w_account1]
            w_elo_before2 = current_elos_player[w_account2]
            w_elo_before3 = current_elos_player[w_account3]
            w_elo_before4 = current_elos_player[w_account4]
            w_elo_before5 = current_elos_player[w_account5]
            #print(w_elo_before1)
            mean_w_elo_before = np.mean(
                [int(w_elo_before1),
                int(w_elo_before2),
                int(w_elo_before3),
                int(w_elo_before4),
                int(w_elo_before5)
                ])
            l_elo_before1 = current_elos_player[l_account1]
            l_elo_before2 = current_elos_player[l_account2]
            l_elo_before3 = current_elos_player[l_account3]
            l_elo_before4 = current_elos_player[l_account4]
            l_elo_before5 = current_elos_player[l_account5]
            mean_l_elo_before = np.mean([
                int(l_elo_before1),
                int(l_elo_before2),
                int(l_elo_before3),
                int(l_elo_before4),
                int(l_elo_before5)
            ])
            # Update on game results
            change_elo = elo.elo_score_constant(mean_w_elo_before,mean_l_elo_before,k_factor)
            #change_elo = elo_player.elo_score_duration_diff(mean_w_elo_before, mean_l_elo_before,duration)
            # Save updated elos
            data_total_info.at[idx,'win_team_elo_player'] = mean_w_elo_before
            data_total_info.at[idx,'Lose_team_elo_player'] = mean_l_elo_before

            mean_w_elo_after, mean_l_elo_after = elo.update_elo_constant_k(mean_w_elo_before, mean_l_elo_before,k_factor)

            w_elo_after1=w_elo_before1 + change_elo
            l_elo_after1=l_elo_before1 - change_elo 
            w_elo_after2=w_elo_before2 + change_elo
            l_elo_after2=l_elo_before2 - change_elo 
            w_elo_after3=w_elo_before3 + change_elo
            l_elo_after3=l_elo_before3 - change_elo 
            w_elo_after4=w_elo_before4 + change_elo
            l_elo_after4=l_elo_before4 - change_elo 
            w_elo_after5=w_elo_before5 + change_elo
            l_elo_after5=l_elo_before5 - change_elo

            current_elos_player[w_account1] = w_elo_after1
            current_elos_player[l_account1] = l_elo_after1
            current_elos_player[w_account2] = w_elo_after2
            current_elos_player[l_account2] = l_elo_after2
            current_elos_player[w_account3] = w_elo_after3
            current_elos_player[l_account3] = l_elo_after3
            current_elos_player[w_account4] = w_elo_after4
            current_elos_player[l_account4] = l_elo_after4
            current_elos_player[w_account5] = w_elo_after5
            current_elos_player[l_account5] = l_elo_after5

            # 如果新的战队之前没有出现过，通过选手的elo评分来给队伍定下基准分
            w_id = row.W_team_id
            l_id = row.L_team_id


            w_elo_before = current_elos_team[w_id]
            l_elo_before = current_elos_team[l_id]
            w_team_times = current_count[w_id]
            l_team_times = current_count[l_id]
            w_team_times, l_team_times = w_team_times+1 ,l_team_times+1   # 计算出战队到最新打了多少次比赛
            current_count[w_id] = w_team_times
            current_count[l_id] = l_team_times
            w_elo_after, l_elo_after = elo.update_elo_constant_k(w_elo_before, l_elo_before, k_factor)
            if current_elos_team[w_id] == mean_elo and current_count[w_id] == 1.0:
                current_elos_team[w_id] = mean_w_elo_after
                data_total_info.at[idx,'win_team_elo_team'] = mean_w_elo_before
            else:
                current_elos_team[w_id] = w_elo_after
                data_total_info.at[idx,'win_team_elo_team'] = w_elo_before

            if current_elos_team[l_id] == mean_elo and current_count[l_id] == 1.0:
                current_elos_team[l_id] = mean_l_elo_after
                data_total_info.at[idx,'Lose_team_elo_team'] = mean_l_elo_before

            else:
                current_elos_team[l_id] = l_elo_after
                data_total_info.at[idx,'Lose_team_elo_team'] = l_elo_before
        
        data_total_info['dire_team_id']= data_total_info.dire_team
        data_total_info['radiant_team_id'] = data_total_info.radiant_team
        ## win_percent
        expected_list = []
        for row in data_total_info.itertuples():
            w_elo = row.win_team_elo_team
            l_elo = row.Lose_team_elo_team
            w_expected = elo.expected_result(w_elo, l_elo)
            expected_list.append(w_expected)
        data_total_info['win_predict'] = expected_list
        data_total_info['lose_predict'] = 1-data_total_info.win_predict
        result=[]
        for row in data_total_info.itertuples():
            if row.win_predict>0.5:
                result.append(1)
            else:
                result.append(0)
        data_total_info['result']=result
        return(data_total_info)
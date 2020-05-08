import numpy as np
import pandas as pd
import itertools

class elo:
    def __init__(self):
        self.k_factor=32
    def update_elo(self,winner_elo, loser_elo,tier='proef'): #通过不同联赛给予不同k值的结果
        """
        https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details
        """
        expected_win = self.expected_result(winner_elo, loser_elo)
        if tier =='premium':
            k_factor=16
        else:
            k_factor=32
        change_in_elo = k_factor * (1-expected_win)
        winner_elo += change_in_elo
        loser_elo -= change_in_elo
        return winner_elo, loser_elo

    def update_elo_team_score(self,winner_elo,loser_elo,k_score_higher=16,k_score_lower=32, elo_score_standard=1800,): #通过战队的elo分值来判断k值的大小
        expected_win = self.expected_result(winner_elo, loser_elo)
        if winner_elo >= elo_score_standard:
            k_score_winner=k_score_higher
        else:
            k_score_winner=k_score_lower
        if loser_elo >=elo_score_standard:
            k_score_loser=k_score_higher
        else:
            k_score_loser=k_score_lower
        change_in_elo_winner = k_score_winner * (1-expected_win)
        change_in_elo_loser = k_score_loser * (1-expected_win)
        winner_elo += change_in_elo_winner
        loser_elo -= change_in_elo_loser
        return winner_elo, loser_elo
    
    def update_elo_last(self,winner_elo, loser_elo, w_team_before, l_team_before, k_score_last=16, k_score_last2=32):
        
        #通过上一场比赛的胜负来给出不同k值的大小
        
        expected_win = self.expected_result(winner_elo, loser_elo)
        if w_team_before == 1 and l_team_before ==0:
            k_factor=k_score_last
        else:
            k_factor=k_score_last2
        change_in_elo = k_factor * (1-expected_win)
        winner_elo += change_in_elo
        loser_elo -= change_in_elo
        return winner_elo, loser_elo
    
    def update_elo_recent(self,winner_elo, loser_elo,recent, k_score_recent1=16, k_score_recent2=32):

        # 通过最近是否有比赛来给出不同k值的大小
        expected_win = self.expected_result(winner_elo, loser_elo)
        if recent == 0:
            k_factor=k_score_recent1
        else:
            k_factor=k_score_recent2
        change_in_elo = k_factor * (1-expected_win)
        winner_elo += change_in_elo
        loser_elo -= change_in_elo
        return winner_elo, loser_elo

    def update_elo_k_16(self,winner_elo, loser_elo): # 固定k值为16的结果
        """
        https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details
        """
        expected_win = self.expected_result(winner_elo, loser_elo)
        change_in_elo = 16 * (1-expected_win)
        winner_elo += change_in_elo
        loser_elo -= change_in_elo
        return winner_elo, loser_elo
    
    def update_elo_constant_k(self,winner_elo, loser_elo, k_score=16): #估计k值 默认为16
        """
        https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details
        """
        expected_win = self.expected_result(winner_elo, loser_elo)
        change_in_elo = k_score * (1-expected_win)
        winner_elo += change_in_elo
        loser_elo -= change_in_elo
        return winner_elo, loser_elo
    
    
    
    def updated_elo_diff_duration(self,winner_elo, loser_elo, duration): # 通过比赛的持续时间来改变k值
        expected_win = self.expected_result(winner_elo, loser_elo)
        if duration >= 3600:
            k_factor = 16
        elif duration>=2000:
            k_factor = 32
        elif duration>=600:
            k_factor = 64
        else:
            k_factor = 128
        change_in_elo = k_factor * (1-expected_win)
        winner_elo += change_in_elo
        loser_elo -= change_in_elo
        return winner_elo, loser_elo
    
    
    
    def expected_result(self,elo_a, elo_b):          # 获胜概率
        expect_a = 1.0/(1+10**((elo_b - elo_a)/400))
        return expect_a
    
    def elo_score_diff_k_factor(self,winner_elo,lose_elo,tier):
        
        expected_win = self.expected_result(winner_elo,lose_elo)
        if tier =='premium':
            k_factor = 16
        else:
            k_factor = 32
        change_elo=k_factor*(1-expected_win)
        return change_elo

    def elo_score_const_k_factor(self,winner_elo,lose_elo):

        expected_win = self.expected_result(winner_elo,lose_elo)
        change_elo=self.k_factor*(1-expected_win)
        return change_elo
    
    def elo_score_recent_game(self,winner_elo,lose_elo,recent,k_score_recent1=16, k_score_recent2=32):

        expected_win = self.expected_result(winner_elo,lose_elo)
        if recent == 0:
            k_factor=k_score_recent1
        else:
            k_factor=k_score_recent2
        change_elo=k_factor*(1-expected_win)
        return change_elo
        
    def elo_score_k_16(self,winner_elo,lose_elo):

        expected_win = self.expected_result(winner_elo,lose_elo)

        change_elo=16*(1-expected_win)
        return change_elo
    
    def elo_score_constant(self,winner_elo,lose_elo,k_score=16):

        expected_win = self.expected_result(winner_elo,lose_elo)

        change_elo=k_score*(1-expected_win)
        return change_elo
    
    def elo_score_duration_diff(self,winner_elo,lose_elo,duration):
        expected_win = self.expected_result(winner_elo,lose_elo)
        if duration >= 3600:
            k_factor = 16
        elif duration>=2000:
            k_factor = 32
        elif duration>=600:
            k_factor = 64
        else:
            k_factor = 128
        change_elo=k_factor*(1-expected_win)
        return change_elo
    
'''
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
            tier = row.tier
            start_time = row.start_time
            current_time = row.current_time
            duration = row.duration
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
            w_elo_after, l_elo_after = self.update_elo_recent(w_elo_before, l_elo_before, recent_game, k_score_recent1, k_score_recent2)
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
            w_expected = elo.expected_result(self, w_elo, l_elo)
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
        current_count = np.zeros(n_teams)
        last_start_time = np.zeros(shape=n_teams)
        last_win_before = np.zeros(shape=(n_teams))
        for row in Major_chongqing_major_Elo.itertuples():
            idx = row.Index
            w_id = row.W_team_id
            l_id = row.L_team_id
            tier = row.tier
            start_time = row.start_time
            #current_time = row.current_time
            duration = row.duration
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
            w_elo_after, l_elo_after = self.update_elo_constant_k(w_elo_before, l_elo_before, k_score)
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
            w_expected = elo.expected_result(self, w_elo, l_elo)
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
            tier = row.tier
            start_time = row.start_time
            current_time = row.current_time
            duration = row.duration
            recent_game =1 if start_time > (current_time - 5270400) else 0
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
            w_elo_after, l_elo_after = self.update_elo_last(w_elo_before, l_elo_before, w_team_last, l_team_last,k_score_last, k_score_last2)
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
            w_expected = elo.expected_result(self, w_elo, l_elo)
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
    
    def player_elo_recent(self, data_total_info,total_players_id,k_score_recent1=16, k_score_recent2=32):
        #dota_team_id=set(list(data_total_info.W_id)+list(data_total_info.L_id))
        #dota_team_id=pd.DataFrame(list(dota_team_id))
        #dota_team_id.index=dota_team_id[0]
        #dota_team_id['team_id']=range(len(dota_team_id))
        
        #W_team_id=[]
        #L_team_id=[]
        mean_elo=1000.0
        n_players = len(total_players_id)
        #n_teams = len(dota_team_id)
        current_elos_player = np.ones(shape=(n_players))*mean_elo
        #current_elos_team = np.ones(shape=(n_teams))*mean_elo
        #current_count = np.zeros(n_teams)
        #last_start_time = np.zeros(shape=n_teams)
        #last_win_before = np.zeros(shape=(n_teams))

        #for i in range(len(data_total_info)):
        #    W_team_id.append(dota_team_id['team_id'][data_total_info['W_id'][i]])
        #    L_team_id.append(dota_team_id['team_id'][data_total_info['L_id'][i]])
        #data_total_info['W_team_id']=W_team_id
        #data_total_info['L_team_id']=L_team_id
        for row in data_total_info.itertuples():

            tier = row.tier
            idx = row.Index
            duration = row.duration
            start_time = row.start_time
            current_time = row.current_time
            recent_game =1 if start_time > (current_time - 5270400) else 0

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
            change_elo = self.elo_score_recent_game(mean_w_elo_before,mean_l_elo_before,recent_game,k_score_recent1, k_score_recent2)
            #change_elo = elo_player.elo_score_duration_diff(mean_w_elo_before, mean_l_elo_before,duration)
            # Save updated elos
            data_total_info.at[idx, "w_elo_before_game1"] = w_elo_before1
            data_total_info.at[idx, "l_elo_before_game1"] = l_elo_before1
            data_total_info.at[idx, "w_elo_after_game1"] = w_elo_before1 + change_elo
            data_total_info.at[idx, "l_elo_after_game1"] = l_elo_before1 - change_elo
            data_total_info.at[idx, "w_elo_before_game2"] = w_elo_before2
            data_total_info.at[idx, "l_elo_before_game2"] = l_elo_before2
            data_total_info.at[idx, "w_elo_after_game2"] = w_elo_before2 + change_elo
            data_total_info.at[idx, "w_elo_after_game2"] = l_elo_before2 - change_elo
            data_total_info.at[idx, "w_elo_before_game3"] = w_elo_before3
            data_total_info.at[idx, "l_elo_before_game3"] = l_elo_before3
            data_total_info.at[idx, "w_elo_after_game3"] = w_elo_before3 + change_elo
            data_total_info.at[idx, "l_elo_after_game3"] = l_elo_before3 - change_elo
            data_total_info.at[idx, "w_elo_before_game4"] = w_elo_before4
            data_total_info.at[idx, "l_elo_before_game4"] = l_elo_before4
            data_total_info.at[idx, "w_elo_after_game4"] = w_elo_before4 + change_elo
            data_total_info.at[idx, "l_elo_after_game4"] = l_elo_before4 - change_elo
            data_total_info.at[idx, "w_elo_before_game5"] = w_elo_before5
            data_total_info.at[idx, "l_elo_before_game5"] = l_elo_before5
            data_total_info.at[idx, "w_elo_after_game5"] = w_elo_before5 + change_elo
            data_total_info.at[idx, "l_elo_after_game5"] = l_elo_before5 - change_elo
            data_total_info.at[idx,'win_team_elo_player'] = mean_w_elo_before
            data_total_info.at[idx,'Lose_team_elo_player'] = mean_l_elo_before

            #mean_w_elo_after, mean_l_elo_after = self.update_elo_recent(mean_w_elo_before, mean_l_elo_before,recent_game)

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
            #w_id = row.W_team_id
            #l_id = row.L_team_id


            #w_elo_before = current_elos_team[w_id]
            #l_elo_before = current_elos_team[l_id]
            #w_team_times = current_count[w_id]
            #l_team_times = current_count[l_id]
            #w_team_last_start_time = last_start_time[w_id]
            #l_team_last_start_time = last_start_time[l_id]
            #w_team_times, l_team_times = w_team_times+1 ,l_team_times+1   # 计算出战队到最新打了多少次比赛
            #current_count[w_id] = w_team_times
            #current_count[l_id] = l_team_times
            #w_elo_after, l_elo_after = self.update_elo(w_elo_before, l_elo_before)
            #if current_elos_team[w_id] == mean_elo and current_count[w_id] == 1.0:
            #    current_elos_team[w_id] = mean_w_elo_after
            #    data_total_info.at[idx,'win_team_elo_team'] = mean_w_elo_before
            #else:
            #    current_elos_team[w_id] = w_elo_after
            #    data_total_info.at[idx,'win_team_elo_team'] = w_elo_before

            #if current_elos_team[l_id] == mean_elo and current_count[l_id] == 1.0:
            #    current_elos_team[l_id] = mean_l_elo_after
            #    data_total_info.at[idx,'Lose_team_elo_team'] = mean_l_elo_before

            #else:
            #    current_elos_team[l_id] = l_elo_after
            #    data_total_info.at[idx,'Lose_team_elo_team'] = l_elo_before
        
        data_total_info['dire_team_id']= data_total_info.dire_team
        data_total_info['radiant_team_id'] = data_total_info.radiant_team
        ## win_percent
        expected_list = []
        for row in data_total_info.itertuples():
            w_elo = row.win_team_elo_player
            l_elo = row.Lose_team_elo_player
            w_expected = self.expected_result(w_elo, l_elo)
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

    def player_elo_constant(self, data_total_info,total_players_id,k_factor=16):
        #dota_team_id=set(list(data_total_info.W_id)+list(data_total_info.L_id))
        #dota_team_id=pd.DataFrame(list(dota_team_id))
        #dota_team_id.index=dota_team_id[0]
        #dota_team_id['team_id']=range(len(dota_team_id))
        
        #W_team_id=[]
        #L_team_id=[]
        mean_elo=1000.0
        n_players = len(total_players_id)
        #n_teams = len(dota_team_id)
        current_elos_player = np.ones(shape=(n_players))*mean_elo
        #current_elos_team = np.ones(shape=(n_teams))*mean_elo
        #current_count = np.zeros(n_teams)
        #last_start_time = np.zeros(shape=n_teams)
        #last_win_before = np.zeros(shape=(n_teams))

        #for i in range(len(data_total_info)):
        #    W_team_id.append(dota_team_id['team_id'][data_total_info['W_id'][i]])
        #    L_team_id.append(dota_team_id['team_id'][data_total_info['L_id'][i]])
        #data_total_info['W_team_id']=W_team_id
        #data_total_info['L_team_id']=L_team_id
        for row in data_total_info.itertuples():

            tier = row.tier
            idx = row.Index
            duration = row.duration
            start_time = row.start_time
            current_time = row.current_time
            recent_game =1 if start_time > (current_time - 5270400) else 0

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
            change_elo = self.elo_score_constant(mean_w_elo_before,mean_l_elo_before,k_factor)
            #change_elo = elo_player.elo_score_duration_diff(mean_w_elo_before, mean_l_elo_before,duration)
            # Save updated elos
            data_total_info.at[idx,'win_team_elo_player'] = mean_w_elo_before
            data_total_info.at[idx,'Lose_team_elo_player'] = mean_l_elo_before

            #mean_w_elo_after, mean_l_elo_after = self.update_elo_recent(mean_w_elo_before, mean_l_elo_before,recent_game)

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
            #w_id = row.W_team_id
            #l_id = row.L_team_id


            #w_elo_before = current_elos_team[w_id]
            #l_elo_before = current_elos_team[l_id]
            #w_team_times = current_count[w_id]
            #l_team_times = current_count[l_id]
            #w_team_last_start_time = last_start_time[w_id]
            #l_team_last_start_time = last_start_time[l_id]
            #w_team_times, l_team_times = w_team_times+1 ,l_team_times+1   # 计算出战队到最新打了多少次比赛
            #current_count[w_id] = w_team_times
            #current_count[l_id] = l_team_times
            #w_elo_after, l_elo_after = self.update_elo(w_elo_before, l_elo_before)
            #if current_elos_team[w_id] == mean_elo and current_count[w_id] == 1.0:
            #    current_elos_team[w_id] = mean_w_elo_after
            #    data_total_info.at[idx,'win_team_elo_team'] = mean_w_elo_before
            #else:
            #    current_elos_team[w_id] = w_elo_after
            #    data_total_info.at[idx,'win_team_elo_team'] = w_elo_before

            #if current_elos_team[l_id] == mean_elo and current_count[l_id] == 1.0:
            #    current_elos_team[l_id] = mean_l_elo_after
            #    data_total_info.at[idx,'Lose_team_elo_team'] = mean_l_elo_before

            #else:
            #    current_elos_team[l_id] = l_elo_after
            #    data_total_info.at[idx,'Lose_team_elo_team'] = l_elo_before
        
        data_total_info['dire_team_id']= data_total_info.dire_team
        data_total_info['radiant_team_id'] = data_total_info.radiant_team
        ## win_percent
        expected_list = []
        for row in data_total_info.itertuples():
            w_elo = row.win_team_elo_player
            l_elo = row.Lose_team_elo_player
            w_expected = self.expected_result(w_elo, l_elo)
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
    
    def player_elo_last_game(self, data_total_info,total_players_id,k_factor=16):
        #dota_team_id=set(list(data_total_info.W_id)+list(data_total_info.L_id))
        #dota_team_id=pd.DataFrame(list(dota_team_id))
        #dota_team_id.index=dota_team_id[0]
        #dota_team_id['team_id']=range(len(dota_team_id))
        
        #W_team_id=[]
        #L_team_id=[]
        mean_elo=1000.0
        n_players = len(total_players_id)
        #n_teams = len(dota_team_id)
        current_elos_player = np.ones(shape=(n_players))*mean_elo
        #current_elos_team = np.ones(shape=(n_teams))*mean_elo
        #current_count = np.zeros(n_teams)
        #last_start_time = np.zeros(shape=n_teams)
        #last_win_before = np.zeros(shape=(n_teams))

        #for i in range(len(data_total_info)):
        #    W_team_id.append(dota_team_id['team_id'][data_total_info['W_id'][i]])
        #    L_team_id.append(dota_team_id['team_id'][data_total_info['L_id'][i]])
        #data_total_info['W_team_id']=W_team_id
        #data_total_info['L_team_id']=L_team_id
        for row in data_total_info.itertuples():

            tier = row.tier
            idx = row.Index
            duration = row.duration
            start_time = row.start_time
            current_time = row.current_time
            recent_game =1 if start_time > (current_time - 5270400) else 0

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
            change_elo = self.elo_score_constant(mean_w_elo_before,mean_l_elo_before,k_factor)
            #change_elo = elo_player.elo_score_duration_diff(mean_w_elo_before, mean_l_elo_before,duration)
            # Save updated elos
            data_total_info.at[idx,'win_team_elo_player'] = mean_w_elo_before
            data_total_info.at[idx,'Lose_team_elo_player'] = mean_l_elo_before

            #mean_w_elo_after, mean_l_elo_after = self.update_elo_recent(mean_w_elo_before, mean_l_elo_before,recent_game)

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
            #w_id = row.W_team_id
            #l_id = row.L_team_id


            #w_elo_before = current_elos_team[w_id]
            #l_elo_before = current_elos_team[l_id]
            #w_team_times = current_count[w_id]
            #l_team_times = current_count[l_id]
            #w_team_last_start_time = last_start_time[w_id]
            #l_team_last_start_time = last_start_time[l_id]
            #w_team_times, l_team_times = w_team_times+1 ,l_team_times+1   # 计算出战队到最新打了多少次比赛
            #current_count[w_id] = w_team_times
            #current_count[l_id] = l_team_times
            #w_elo_after, l_elo_after = self.update_elo(w_elo_before, l_elo_before)
            #if current_elos_team[w_id] == mean_elo and current_count[w_id] == 1.0:
            #    current_elos_team[w_id] = mean_w_elo_after
            #    data_total_info.at[idx,'win_team_elo_team'] = mean_w_elo_before
            #else:
            #    current_elos_team[w_id] = w_elo_after
            #    data_total_info.at[idx,'win_team_elo_team'] = w_elo_before

            #if current_elos_team[l_id] == mean_elo and current_count[l_id] == 1.0:
            #    current_elos_team[l_id] = mean_l_elo_after
            #    data_total_info.at[idx,'Lose_team_elo_team'] = mean_l_elo_before

            #else:
            #    current_elos_team[l_id] = l_elo_after
            #    data_total_info.at[idx,'Lose_team_elo_team'] = l_elo_before
        
        data_total_info['dire_team_id']= data_total_info.dire_team
        data_total_info['radiant_team_id'] = data_total_info.radiant_team
        ## win_percent
        expected_list = []
        for row in data_total_info.itertuples():
            w_elo = row.win_team_elo_player
            l_elo = row.Lose_team_elo_player
            w_expected = self.expected_result(w_elo, l_elo)
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
            tier = row.tier
            start_time = row.start_time
            duration = row.duration
            w_elo_before = current_elos[w_id]
            l_elo_before = current_elos[l_id]
            w_team_times = current_count[w_id]
            l_team_times = current_count[l_id]
            w_team_last_start_time = last_start_time[w_id]
            l_team_last_start_time = last_start_time[l_id]
            # Update on game results
            w_elo_after, l_elo_after = self.update_elo_constant_k(w_elo_before, l_elo_before, k_score)
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
            idx = row.Index
            w_id = row.W_team_id
            l_id = row.L_team_id
            tier = row.tier
            start_time = row.start_time
            #current_time = row.current_time
            duration = row.duration
            #lairecent_game =1 if start_time > (current_time - 5270400) else 0
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
            w_elo_after, l_elo_after = self.update_elo_last(w_elo_before, l_elo_before, w_team_last, l_team_last,k_score_last, k_score_last2)
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
        last_start_time = np.zeros(shape=n_teams)
        last_win_before = np.zeros(shape=(n_teams))

        for i in range(len(data_total_info)):
            W_team_id.append(dota_team_id['team_id'][data_total_info['W_id'][i]])
            L_team_id.append(dota_team_id['team_id'][data_total_info['L_id'][i]])
        data_total_info['W_team_id']=W_team_id
        data_total_info['L_team_id']=L_team_id
        for row in data_total_info.itertuples():

            tier = row.tier
            idx = row.Index
            duration = row.duration
            start_time = row.start_time
            current_time = row.current_time
            recent_game =1 if start_time > (current_time - 5270400) else 0

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
            change_elo = self.elo_score_constant(mean_w_elo_before,mean_l_elo_before,k_factor)
            #change_elo = elo_player.elo_score_duration_diff(mean_w_elo_before, mean_l_elo_before,duration)
            # Save updated elos
            data_total_info.at[idx,'win_team_elo_player'] = mean_w_elo_before
            data_total_info.at[idx,'Lose_team_elo_player'] = mean_l_elo_before

            mean_w_elo_after, mean_l_elo_after = self.update_elo_constant_k(mean_w_elo_before, mean_l_elo_before,k_factor)

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
            w_team_last_start_time = last_start_time[w_id]
            l_team_last_start_time = last_start_time[l_id]
            w_team_times, l_team_times = w_team_times+1 ,l_team_times+1   # 计算出战队到最新打了多少次比赛
            current_count[w_id] = w_team_times
            current_count[l_id] = l_team_times
            w_elo_after, l_elo_after = self.update_elo_constant_k(w_elo_before, l_elo_before, k_factor)
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
            w_expected = self.expected_result(w_elo, l_elo)
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
    
    
    def player_team_elo_result(self, data_total_info,total_players_id,k_factor=16):
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
        last_start_time = np.zeros(shape=n_teams)
        last_win_before = np.zeros(shape=(n_teams))

        for i in range(len(data_total_info)):
            W_team_id.append(dota_team_id['team_id'][data_total_info['W_id'][i]])
            L_team_id.append(dota_team_id['team_id'][data_total_info['L_id'][i]])
        data_total_info['W_team_id']=W_team_id
        data_total_info['L_team_id']=L_team_id
        for row in data_total_info.itertuples():

            tier = row.tier
            idx = row.Index
            duration = row.duration
            start_time = row.start_time
#            current_time = row.current_time
#            recent_game =1 if start_time > (current_time - 5270400) else 0

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
            change_elo = self.elo_score_constant(mean_w_elo_before,mean_l_elo_before,k_factor)
            #change_elo = elo_player.elo_score_duration_diff(mean_w_elo_before, mean_l_elo_before,duration)
            # Save updated elos
            data_total_info.at[idx,'win_team_elo_player'] = mean_w_elo_before
            data_total_info.at[idx,'Lose_team_elo_player'] = mean_l_elo_before

            mean_w_elo_after, mean_l_elo_after = self.update_elo_constant_k(mean_w_elo_before, mean_l_elo_before,k_factor)

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
            w_team_last_start_time = last_start_time[w_id]
            l_team_last_start_time = last_start_time[l_id]
            w_team_times, l_team_times = w_team_times+1 ,l_team_times+1   # 计算出战队到最新打了多少次比赛
            current_count[w_id] = w_team_times
            current_count[l_id] = l_team_times
            w_elo_after, l_elo_after = self.update_elo_constant_k(w_elo_before, l_elo_before, k_factor)
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
            w_expected = self.expected_result(w_elo, l_elo)
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
        return(current_elos_team)
'''
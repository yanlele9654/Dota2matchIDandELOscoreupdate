# team1_win_rate_bo1\
p = 0.5
# team2_win_rate_bo1 =
q = 1 - p
# bo3:
# team1_win
team1_win_bo3 = p * q * p + p * p + q * p * p
team2_win_bo3 = q * p * q + p * q * q + q * q
# bo5:
team1_win_bo5 = p * p * p + 3 * q * p * p * p + 6 * p * p * q * q * p
team2_win_bo5 = q * q * q + 3 * p * q * q * q + 6 * q * q * p * p * q
# %%
# BO3:
# HDC
Team_1_NEG_15 = p * p
Team_1_POS_15 = 1 - q * q
Team_2_NEG_15 = q * q
Team_2_POS_15 = 1 - p * p
# BO5:
# HDC
Team_1_NEG_25 = p * p * p
Team_1_POS_25 = 1 - q * q * q
Team_2_NEG_25 = q * q * q
Team_2_POS_25 = 1 - p * p * p
Team_1_NEG_15_BO5 = p * p * p + p * p * p * q * 3
Team_1_POS_15_BO5 = 1 - (q * q * q + q * q * q * p * 3)
Team_2_NEG_15_BO5 = q * q * q + q * q * q * p * 3
Team_2_POS_15_BO5 = 1 - (p * p * p + p * p * p * q * 3)


# %%
# 队伍1ELO分数胜率 p1
# 队伍1市场胜负赔率 odds1
# 队伍2市场胜负赔率 odds2
# 本金 Total_amount
# 如果result的值大于0，则返回可以下注，如果result的值小于0，则返回无法下注
result = ((p1 * Total_amount * odds1 - Total_amount) * p1 + ((1 - p1) * Total_amount * odds2 - Total_amount) * (1 - p2))

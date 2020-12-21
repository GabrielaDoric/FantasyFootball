import csv
import pandas as pd
import numpy as np

PATH_TO_CSV = './instances/instance1.csv'
'''

df = pd.read_csv(PATH_TO_CSV, names=["ID", "Position", "Name", "Club", "Points", "Price"])
# print (df)

worst_priced = df.loc[(df['Price'] <= 4)]
# print ((worst_priced))



best = df.nlargest(10, ['Price'])
# print (best)
'''



def pick_worst_4(df):
    worst_players = []

    worst_gk = df.loc[(df['Position'] == 'GK')].nsmallest(1, ['Price']).values.tolist()
    worst_players.extend(worst_gk)

    worst_def = df.loc[(df['Position'] == 'DEF')].nsmallest(2, ['Price']).values.tolist()
    worst_players.extend(worst_def)

    worst_fw = df.loc[(df['Position'] == 'FW')].nsmallest(1, ['Price']).values.tolist()
    worst_players.extend(worst_fw)

    # print (np.array(worst_players))
    return worst_players


def pick_n_best_players(df):
    best_players = []

    best_gk = df.loc[(df['Position'] == 'GK')].nlargest(5, ['Price']).values.tolist()
    best_players.extend(best_gk)

    best_def = df.loc[(df['Position'] == 'DEF')].nlargest(10, ['Price']).values.tolist()
    best_players.extend(best_def)

    best_fw = df.loc[(df['Position'] == 'FW')].nlargest(10, ['Price']).values.tolist()
    best_players.extend(best_fw)

    best_mid = df.loc[(df['Position'] == 'MID')].nlargest(10, ['Price']).values.tolist()
    best_players.extend(best_mid)

    # print (np.array(worst_players))
    return best_players


def moj_knapsack(best_players,prices, points, C, n, counter):
    #print(C)
    #print(counter)
    if n == 0:
        return 0

    if counter == 11:
        indices = []
        return 0

    if (prices[n - 1] > C):
        # print ('drugi')
        return moj_knapsack(best_players,prices, points, C, n - 1, counter)

    else:
        return max(points[n - 1] + moj_knapsack(best_players,prices, points, C - prices[n - 1], n - 1,counter+1),
                   moj_knapsack(best_players,prices, points, C, n - 1,counter+1))




def knapsack1(W, wt, val, n, best_players):

    odabrani=[]

    #print('hhhhhhhhhhhhhhh', best_players.shape)

    dp=np.zeros((n,int(W)+1,11))
    #print (dp.shape)

    for i in range(n):
        #odabrani.append(best_players[i])
        #print (odabrani)
        id, pos, name, club, points, price = best_players[i]
        #print (best_players[i])
        #odabrani.append(best_players[i])
        flag=0
        for j in range(int(W)+1):
            for k in range(0,11):
                #print ('heeee',best_players[i])
                if (i>0) and wt[i-1] <= j:
                    #print(odabrani)
                    if (val[i - 1] + dp[i - 1][j - wt[i - 1]][k-1])>(dp[i - 1][j][k]):
                        flag = 1
                    dp[i][j][k] = max(val[i - 1] + dp[i - 1][j - wt[i - 1]][k-1], dp[i - 1][j][k])

                else:
                    #print (odabrani)
                    #print ('he',odabrani[0])
                    #print ('aa',best_players[i])
                    #if best_players[i] in odabrani:
                        #odabrani.remove(best_players[i])
                    if (i>0):
                        dp[i][j][k] = dp[i - 1][j][k]

        if (flag==1):
            odabrani.append(best_players[i])

    for sth in odabrani:
        print (sth)

    print (len(odabrani))


    # find indices of players

    dp_1 = dp[:, :, 0]

    list_of_players = []
    for x in range(n):
        if dp_1[x][int(W)] == dp_1[n-1][int(W)]:
            w = W
            i = x

            while (i > 0 and w > 0 and len(list_of_players) < 11):
                if (dp_1[i][int(w)] == dp_1[i - 1][int(w) - wt[i - 1]] + val[i - 1]):
                    list_of_players.append(i)
                    w = w - wt[i - 1]
                    i = i - 1
                else:
                    i = i - 1



    return list_of_players, dp[n-1][int(W)][10]


if __name__ == '__main__':
    lineup = []
    # setup15=np.array(setup15)

    # read CSV
    df = pd.read_csv(PATH_TO_CSV, names=["ID", "Position", "Name", "Club", "Points", "Price"])

    worst_4 = pick_worst_4(df)

    # print (np.array(worst_4))

    spent_money = 0
    for i in worst_4:
        spent_money += i[5]
    spent_money = round(spent_money, 1)

    lineup.extend(worst_4)

    best = pick_n_best_players(df)
    # print((np.array(best)))

    he = np.array(best)
    # print (he[0][1])

    points = []
    prices = []
    for i in best:
        points.append(i[4])
        prices.append(int(i[5] * 10))

    val = points
    wt = prices
    W = 1000 - spent_money * 10

    n = len(val)

    # print (n)
    # print (W)


    #player_indices, rez = knapsack1(W, wt, val, n, np.array(best))
    #print (rez)
    #for j in player_indices:
    #    print (best[j-1])

    # print (np.array(best))

    rez=dobit = moj_knapsack(np.array(best),prices, points, W, n, counter=0)
    print (rez)
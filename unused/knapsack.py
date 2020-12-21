import csv
import pandas as pd
import numpy as np

PATH_TO_CSV = './instances/instance1.csv'

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

    best_gk = df.loc[(df['Position'] == 'GK')].nlargest(4, ['Price']).values.tolist()
    best_players.extend(best_gk)

    best_def = df.loc[(df['Position'] == 'DEF')].nlargest(5, ['Price']).values.tolist()
    best_players.extend(best_def)

    best_fw = df.loc[(df['Position'] == 'FW')].nlargest(6, ['Price']).values.tolist()
    best_players.extend(best_fw)

    best_mid = df.loc[(df['Position'] == 'MID')].nlargest(5, ['Price']).values.tolist()
    best_players.extend(best_mid)

    # print (np.array(worst_players))
    return best_players

def knapSack_din(W, wt, val, n, pamti):
    W=int(W)
    K = [[0 for x in range(W + 1)] for x in range(n + 1)]
    #print (W)
    #print (n)

    #K=[n+1][W+1]
    '''
    "    K=[][]
        for i in range (W+1):
            for j in range (n+1):
                K[i][j]=0
    '''



    # Build table K[][] in bottom up manner
    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i - 1] <= w:
                K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w])
            else:
                K[i][w] = K[i - 1][w]

    return K[n][W]


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


    points = []
    prices = []
    for i in best:
        points.append(i[4])
        prices.append(int(i[5] * 10))

    val = points
    wt = prices
    W = 1000 - spent_money * 10

    n = len(val)

    rez=knapSack_din(W, wt, val, n)
    print (rez)
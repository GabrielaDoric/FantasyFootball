import csv
import pandas as pd
import numpy as np

PATH_TO_CSV = './instances/instance1.csv'
'''


with open(PATH_TO_CSV) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    csv_reader = list(csv_reader)
    #for row in csv_reader:
        #print (row)
    print (len(csv_reader))

    itemDict = {item[0]: item[1:] for item in csv_reader}
    print ((itemDict[1]))
'''

df = pd.read_csv(PATH_TO_CSV, names=["ID", "Position", "Name", "Club", "Points", "Price"])
# print (df)

worst_priced = df.loc[(df['Price'] <= 4)]
# print ((worst_priced))

arr = df.to_numpy()
# print ((arr))

best = df.nlargest(10, ['Price'])
# print (best)

picked_15 = []
# izaberi najgoreg golmana i dodaj ga u 15
worst_gk = df.loc[(df['Position'] == 'GK')].nsmallest(1, ['Price']).values.tolist()
picked_15.extend(worst_gk)

worst_def = df.loc[(df['Position'] == 'DEF')].nsmallest(2, ['Price']).values.tolist()
picked_15.extend(worst_def)

worst_fw = df.loc[(df['Position'] == 'FW')].nsmallest(1, ['Price']).values.tolist()
picked_15.extend(worst_fw)

best = df.loc[(df['Position'] == 'MID')].nlargest(10, ['Price'])


# print(best)


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


def moj_knapsack(prices, points, C, n, indices, counter, num_players=11):
    print(C)
    print(counter)
    if n == 0:
        return 0

    if counter == 11:
        indices = []
        return 0

    if (prices[n - 1] > C):
        # print ('drugi')
        return moj_knapsack(prices, points, C, n - 1, indices, counter)

    else:
        indices.append(n - 1)
        return max(points[n - 1] + moj_knapsack(prices, points, C - prices[n - 1], n - 1, indices, counter + 1),
                   moj_knapsack(prices, points, C, n - 1, indices, counter + 1))


def knapSack_din(W, wt, val, n, pamti):
    W = int(W)
    K = [[0 for x in range(W + 1)] for x in range(n + 1)]
    # print (W)
    # print (n)

    # K=[n+1][W+1]
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


def knapSack_3d(W, wt, val, n):
    W = int(W)
    K = [[[0 for x in range(11)] for x in range(W + 1)] for x in range(n + 1)]
    # K = [[[0 for x in range(W+1)] for x in range(n + 1)] for x in range(11)]

    # Build table K[][] in bottom up manner

    # for each element given
    for i in range(n + 1):
        # for each possible weight value
        for w in range(W + 1):
            # for each case where the total elements are less then the constraint
            for j in range(0, 11):
                if i == 0 or w == 0 or j == 0:
                    # print (j)
                    K[i][w][j] = 0
                elif wt[i - 1] <= w:
                    K[i][w][j] = max(val[i - 1] + K[i - 1][w - wt[i - 1]][j], K[i - 1][w][j])
                else:
                    K[i][w][j] = K[i - 1][w][j]

    # return K[11][W+1][n+1]
    # return K[n+1][W+1][11]
    return K[W + 1][11][n + 1]


def knapsack1(W, wt, val, n):
    dp=np.zeros((n,int(W)+1,11))

    for i in range(n):
        for j in range(int(W)+1):
            for k in range(0,11):
                if wt[i-1] <= j:
                    dp[i][j][k] = max(val[i - 1] + dp[i - 1][j - wt[i - 1]][k-1], dp[i - 1][j][k])
                else:

                    dp[i][j][k] = dp[i - 1][j][k]

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

    # print(knapsack(wt, val, W, n))

    # print(knapsack(prices, points, W, n))
    indices = []
    # dobit = moj_knapsack(prices, points, W, n, indices, counter=0)
    # print('heeee', br)
    # print('heeee', dobit)

    # print ((indices))

    pamti = []
    # rez=knapSack_din(W, wt, val, n,pamti)
    # print (rez)

    # rez=knapSack_3d(W, wt, val, n)
    # print(rez)

    player_indices, rez = knapsack1(W, wt, val, n, np.array(best))
    print (rez)
    #for j in player_indices:
    #    print (best[j-1])

    # print (np.array(best))

import pandas as pd
import numpy as np
from operator import itemgetter

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

    best_gk = df.loc[(df['Position'] == 'GK')].nlargest(20, ['Price']).values.tolist()
    best_players.extend(best_gk)

    best_def = df.loc[(df['Position'] == 'DEF')].nlargest(20, ['Price']).values.tolist()
    best_players.extend(best_def)

    best_fw = df.loc[(df['Position'] == 'FW')].nlargest(20, ['Price']).values.tolist()
    best_players.extend(best_fw)

    best_mid = df.loc[(df['Position'] == 'MID')].nlargest(15, ['Price']).values.tolist()
    best_players.extend(best_mid)

    # print (np.array(worst_players))
    return best_players


def greedy_knapsack(best_players,prices, points, W, n):
    lineup=[]
    lineup_price=0
    lineup_points=0

    counter=0
    taken_positions=[]
    clubs_from=[]

    sorted_players = sorted(best_players, key=lambda x: x[4])
    #print (sorted_players)
    #sorted_players= (sorted_players)
    #print (type(sorted_players))

    while len(sorted_players)>0 and counter<11:
        player = sorted_players.pop()
        id,position,name,club,points, price=player


        if (position == 'GK' and taken_positions.count('GK') == 1) or (position == 'DEF' and taken_positions.count('DEF') == 3) \
                    or (position == 'MID' and taken_positions.count('MID') == 5) or (position == 'FW' and taken_positions.count('FW') == 2)\
                    or (clubs_from.count(club) == 3):
            continue


        if price + lineup_price <= W:
            counter+=1
            lineup.append(player)
            lineup_price+=price
            lineup_points+=points
            taken_positions.append(position)
            clubs_from.append(club)
        else:
            break

    #print (taken_positions)
    #print (clubs_from)




    #best_players_sorted=sorted(best_players,key=)

    return lineup,lineup_points

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

    igraci, dobit = greedy_knapsack(best,prices, points, W, n)
    print (dobit)
    print (np.array(igraci))

    '''
    lineup=np.array(lineup)
    print (lineup)

    print ('heeee')
    sorted= sorted(lineup,key=itemgetter(1))
    sorted=np.array(sorted)
    print (sorted)
    '''




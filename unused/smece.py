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

    best_gk = df.loc[(df['Position'] == 'GK')].nlargest(5, ['Price']).values.tolist()
    best_players.extend(best_gk)

    best_def = df.loc[(df['Position'] == 'DEF')].nlargest(10, ['Price']).values.tolist()
    best_players.extend(best_def)

    best_fw = df.loc[(df['Position'] == 'FW')].nlargest(10, ['Price']).values.tolist()
    best_players.extend(best_fw)

    best_mid = df.loc[(df['Position'] == 'MID')].nlargest(20, ['Price']).values.tolist()
    best_players.extend(best_mid)

    # print (np.array(worst_players))

    return best_gk, best_def, best_fw, best_mid, best_players


def greedy_knapsack(best_players, prices, points, W, n):
    lineup = []
    lineup_price = 0
    lineup_points = 0
    counter = 0
    taken_positions = []
    clubs_from = []

    # best_players = points_per_million(best_players)
    # sorted_players = sorted(best_players, key=lambda x: x[6])

    # best_players = points_per_million(best_players)
    sorted_players = sorted(best_players, key=lambda x: x[4])

    #print(np.array(sorted_players))

    while len(sorted_players) > 0 and counter <= 11:
        player = sorted_players.pop()
        # print (len(sorted_players))
        id, position, name, club, points, price = player

        if (position == 'GK' and taken_positions.count('GK') == 1) or (
                position == 'DEF' and taken_positions.count('DEF') == 3) \
                or (position == 'MID' and taken_positions.count('MID') == 5) or (
                position == 'FW' and taken_positions.count('FW') == 2) \
                or (clubs_from.count(club) == 3):
            continue

        #print (84.1 - (price + lineup_price))
        #print ((len(taken_positions)+1)* 4.5)
        if (84.1 - (price + lineup_price)) < (11-(len(taken_positions)+1)) * 4.5:
            continue

        if price + lineup_price <= 84.1:

            counter += 1
            lineup.append(player)
            lineup_price += price
            lineup_points += points
            taken_positions.append(position)
            clubs_from.append(club)

        else:
            break

    # print (taken_positions)
    # print (clubs_from)

    print ('lineup_price',lineup_price)

    # best_players_sorted=sorted(best_players,key=)

    #for player in lineup:
    #    player.pop()

    print(len(lineup))

    return lineup, lineup_points


def pokusaj(best_gk, best_def, best_fw, best_mid, best_players, prices, points, W, n):
    CONSTRAINT_GK = 1
    CONSTRAINT_MID = 5
    CONSTRAINT_FW = 2
    CONTRAINT_DEF = 3

    sorted_gk = sorted(best_gk, key=lambda x: x[4])
    sorted_def = sorted(best_def, key=lambda x: x[4], reverse=True)
    sorted_fw = sorted(best_fw, key=lambda x: x[4], reverse=True)
    sorted_mid = sorted(best_mid, key=lambda x: x[4])

    lineup = []
    lineup_price = 0
    lineup_points = 0

    counter = 0
    taken_positions = []
    clubs_from = []

    # izaberi gk
    lineup.append(sorted_gk.pop())

    while counter < CONSTRAINT_MID:
        counter += 1
        lineup.append(sorted_mid.pop())

    counter = 0
    while counter < CONTRAINT_DEF:
        counter += 1
        lineup.append(sorted_def.pop())

    counter = 0
    while counter < CONSTRAINT_FW:
        counter += 1
        lineup.append(sorted_fw.pop())

    trosak = 0
    for player in lineup:
        trosak += player[5]

    print(trosak)

    print(np.array(lineup))


def points_per_million(players):
    for player in players:
        ppm = player[4] / player[5]
        player.append(ppm)

    return players


def pokusaj_1(best_gk, best_def, best_fw, best_mid, best, prices, points, W, n):
    # print (type(best_gk))
    # print (np.array(best_gk))

    best = points_per_million(best)
    # print(np.array(best))

    sorted_players = sorted(best, key=lambda x: x[6])
    print(np.array(sorted_players))


def df_to_list(df, lista_najgorih):
    nova_lista = df.values.tolist()

    res = list(filter(lambda i: i not in lista_najgorih, nova_lista))

    return res


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

    best_gk, best_def, best_fw, best_mid, best = pick_n_best_players(df)
    # print((np.array(best)))

    #print('sto je worst_4', type(worst_4))
    lista_svih = df_to_list(df, worst_4)
    # print (lista_svih)

    points = []
    prices = []
    for i in best:
        points.append(i[4])
        prices.append(int(i[5] * 10))

    val = points
    wt = prices
    W = 1000 - spent_money * 10
    n = len(val)

    igraci, dobit = greedy_knapsack(lista_svih, prices, points, W, n)
    print(dobit)
    print(np.array(igraci))

    '''
    lineup=np.array(lineup)
    print (lineup)

    print ('heeee')
    sorted= sorted(lineup,key=itemgetter(1))
    sorted=np.array(sorted)
    print (sorted)
    '''

    # pokusaj = pokusaj_1(best_gk, best_def, best_fw, best_mid, best, prices, points, W, n)
    # print (pokusaj)

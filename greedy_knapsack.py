import pandas as pd
import numpy as np


PATH_TO_CSV = './instances/instance1.csv'

def points_per_million(players):
    for player in players:
        ppm = player[4] / player[5]
        player.append(ppm)

    return players


def df_to_list(df, remove_list):
    nova_lista = df.values.tolist()

    res = list(filter(lambda i: i not in remove_list, nova_lista))

    return res

def money_spent(players):
    spent_money = 0
    for i in players:
        spent_money += i[5]
    spent_money = round(spent_money, 1)

    return spent_money


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


def greedy_knapsack(best_players, W):
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

    # print(np.array(sorted_players))

    while len(sorted_players) > 0 and counter <= 11:
        player = sorted_players.pop()
        id, position, name, club, points, price = player

        if (position == 'GK' and taken_positions.count('GK') == 1) or (
                position == 'DEF' and taken_positions.count('DEF') == 3) \
                or (position == 'MID' and taken_positions.count('MID') == 5) or (
                position == 'FW' and taken_positions.count('FW') == 2) \
                or (clubs_from.count(club) == 3):
            continue

        if (W - (price + lineup_price)) < (11 - (len(taken_positions) + 1)) * 4.5:
            continue

        if price + lineup_price <= W:
            counter += 1
            lineup.append(player)
            lineup_price += price
            lineup_points += points
            taken_positions.append(position)
            clubs_from.append(club)

        else:
            break

    print('lineup_price', lineup_price)


    # for player in lineup:
    #    player.pop()

    print('br igraca',len(lineup))

    return lineup, lineup_points





if __name__ == '__main__':
    lineup = []

    INITIAL_BUDGET = 100

    # read CSV
    df = pd.read_csv(PATH_TO_CSV, names=["ID", "Position", "Name", "Club", "Points", "Price"])

    worst_4 = pick_worst_4(df)
    lineup.extend(worst_4)

    #all players does not contain worst_4
    all_players = df_to_list(df, worst_4)
    # print (all_players)



    eleven, profit = greedy_knapsack(all_players, W = INITIAL_BUDGET - money_spent(worst_4))
    print(profit)
    print(np.array(eleven))

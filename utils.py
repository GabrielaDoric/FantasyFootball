import random
import pandas as pd
import numpy as np


def points_per_million(players):
    for player in players:
        ppm = player[4] / player[5]
        player.append(ppm)
    return players


def remove_some_players(init_list, remove_list):
    res = list(filter(lambda i: i not in remove_list, init_list))
    return res


def money_spent(players):
    spent_money = 0
    for i in players: spent_money += i[5]
    spent_money = round(spent_money, 1)
    return spent_money


def pick_worst_4(df):
    worst_players = []

    worst_gk = df.loc[(df['Position'] == 'GK')].nsmallest(1, ['Price']).values.tolist()
    worst_players.extend(worst_gk)

    worst_def = df.loc[(df['Position'] == 'DEF')].nsmallest(2, ['Price']).values.tolist()
    worst_players.extend(worst_def)

    worst_fw = df.loc[(df['Position'] == 'FW')].nsmallest(1, ['Price']).values.tolist()

    # print ('hej',worst_fw[1])
    #worst_players.extend([worst_fw[0]])
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


def write_to_txt(txt_file, worst, best):
    pom = []
    for player in best: pom.append(player[0])
    pom.sort()
    first_row = ",".join(str(x) for x in pom)

    pom = []
    for player in worst: pom.append(player[0])
    pom.sort()
    second_row = ",".join(str(x) for x in pom)

    text_file = open(txt_file, "w")
    text_file.write(first_row)
    text_file.write('\n')
    text_file.write(second_row)
    text_file.close()

    return text_file


def get_players_by_position(players):
    gks = []
    mids = []
    fws = []
    defs = []

    for player in players:
        if player[1] == 'GK':
            gks.append(player)
        elif player[1] == 'MID':
            mids.append(player)
        elif player[1] == 'FW':
            fws.append(player)
        elif player[1] == 'DEF':
            defs.append(player)

    return gks, mids, defs, fws

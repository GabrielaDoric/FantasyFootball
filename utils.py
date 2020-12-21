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


def pick_worst_4(df, backup_formation):
    worst_players = []

    worst_gk = df.loc[(df['Position'] == 'GK')].nsmallest(backup_formation[0], ['Price']).values.tolist()
    worst_players.extend(worst_gk)

    worst_fw = df.loc[(df['Position'] == 'MID')].nsmallest(backup_formation[1], ['Price']).values.tolist()
    worst_players.extend(worst_fw)

    worst_def = df.loc[(df['Position'] == 'DEF')].nsmallest(backup_formation[2], ['Price']).values.tolist()
    worst_players.extend(worst_def)

    worst_fw = df.loc[(df['Position'] == 'FW')].nsmallest(backup_formation[3], ['Price']).values.tolist()
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




def really_greedy(best_players, W, clubs_of_worst, formation):
    lineup = []
    lineup_price = 0
    lineup_points = 0

    taken_positions = []
    clubs_from = []

    sorted_players = sorted(best_players, key=lambda x: x[4])

    counter = 0
    while len(sorted_players) > 0 and counter <= 11:
        player = sorted_players.pop()
        id, position, name, club, points, price = player


        if (position == 'GK' and taken_positions.count('GK') == 1) or (
                position == 'DEF' and taken_positions.count('DEF') == (5-formation[2])) \
                or (position == 'MID' and taken_positions.count('MID') == (5-formation[1])) or (
                position == 'FW' and taken_positions.count('FW') == (3-formation[3])) \
                or (clubs_from.count(club) + clubs_of_worst.count(club) == 3):
            continue

        ## ako ja npr trebam odabrati jos 3 igraca, a cca jedan najgori kosta 4.5, ja moram imati jos minimalno 4.5*3 milijuna
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

    return lineup, lineup_points, lineup_price


def ppm_greedy(best_players, W, clubs_of_worst, formation):
    # clubs_of_worst=['Brighton','Burnley','Sheffield Utd','Arsenal']




    lineup = []
    lineup_price = 0
    lineup_points = 0
    counter = 0
    taken_positions = []
    clubs_from = []

    ### jedina, ali bitna razlika izmedu jako greedy algoritma i points per million
    best_players = points_per_million(best_players)
    sorted_players = sorted(best_players, key=lambda x: x[6])

    while len(sorted_players) > 0 and counter <= 11:
        player = sorted_players.pop()
        id, position, name, club, points, price, ppm = player

        if (position == 'GK' and taken_positions.count('GK') == 1) or (
                position == 'DEF' and taken_positions.count('DEF') == (5-formation[2])) \
                or (position == 'MID' and taken_positions.count('MID') == (5-formation[1])) or (
                position == 'FW' and taken_positions.count('FW') == (3-formation[3])) \
                or (clubs_from.count(club) + clubs_of_worst.count(club) == 3):
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

    for player in best_players:
        player.pop()

    return lineup, lineup_points, lineup_price



def get_profit(lineup):
    sum = 0
    for player in lineup:
        sum += player[4]

    return sum


def get_money_spent(lineup):
    sum = 0
    for player in lineup:
        sum += player[5]

    return sum
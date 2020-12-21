import random

import pandas as pd
import numpy as np

PATH_TO_CSV = './instances/instance1.csv'


def points_per_million(players):
    for player in players:
        ppm = player[4] / player[5]
        player.append(ppm)

    return players


def remove_some_players(nova_lista, remove_list):
    # nova_lista = df.values.tolist()

    res = list(filter(lambda i: i not in remove_list, nova_lista))

    # print (len(nova_lista))
    # print (len(remove_list))
    # print (len(res))

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

    # print('lineup_price', lineup_price)
    # print('br igraca', len(lineup))

    return lineup, lineup_points, lineup_price


def greedy_knapsack_ppm(best_players, W):
    lineup = []
    lineup_price = 0
    lineup_points = 0
    counter = 0
    taken_positions = []
    clubs_from = []

    best_players = points_per_million(best_players)
    sorted_players = sorted(best_players, key=lambda x: x[6])

    # print(np.array(sorted_players))

    while len(sorted_players) > 0 and counter <= 11:
        player = sorted_players.pop()
        id, position, name, club, points, price, ppm = player

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

    # print('lineup_price', lineup_price)

    for player in lineup:
        player.pop()

    # print('br igraca', len(lineup))

    return lineup, lineup_points, lineup_price


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


def local_search_ppm(players, W):
    lineup, profit, lineup_price = greedy_knapsack(players, W)
    prices = [x[5] for x in lineup]
    print('pocetno', lineup_price)

    neighbourhood = []

    all_gks, all_mids, all_defs, all_fws = get_players_by_position(players)
    gsk1, mids1, defs1, fws1 = get_players_by_position(lineup)

    svi_pozicije = [all_gks, all_mids, all_defs, all_fws]
    pozicije = [gsk1, mids1, defs1, fws1]

    for i, pozicija in enumerate(pozicije):
        potencial_substitute = []
        random_player = random.choice(pozicija)

        id, position, name, club, points, price = random_player

        for p in svi_pozicije[i]:
            # ako neizabrani igrac ima istu poziciju kao i ovaj
            # i ako mu je price u rasponu price trenutnog +-1.0
            if p[1] == position and (abs(price - p[5])) <= 1.5:
                potencial_substitute.append(p)

        print(np.array(potencial_substitute))
        print('----------------------')

    return lineup


def local_search(players, W):
    lineup, profit, lineup_price = greedy_knapsack(players, W)

    rez = lineup
    new_lineup = lineup
    prices = [x[5] for x in lineup]
    # print (sum(prices))

    # price_po_igracima=

    gks, mids, defs, fws = get_players_by_position(players)
    gsk1, mids1, defs1, fws1 = get_players_by_position(lineup)

    svi_pozicije = [gks, mids, defs, fws]
    pozicije = [gsk1, mids1, defs1, fws1]

    potencial_substitute = []
    for i, pozicija in enumerate(pozicije):
        random_player = random.choice(pozicija)

        id, position, name, club, points, price = random_player

        for p in svi_pozicije[i]:
            # ako neizabrani igrac ima istu poziciju kao i ovaj
            # i ako mu je price u rasponu price trenutnog +-1.0
            if p[1] == position and (abs(price - p[5])) <= 1.5:
                potencial_substitute.append(p)

        random_substitute = random.choice(potencial_substitute)

        new_lineup.remove(random_player)
        new_lineup.append(random_substitute)

        new_prices = [x[5] for x in new_lineup]

        # print ('nove',sum(new_prices))
        # print('staro', sum(prices))

        if sum(new_prices) > sum(prices) and sum(new_prices) <= W:
            print('istina')
            lineup = new_lineup
            break

        # print (i)
        # print (random_player)

    # pick random from list

    return lineup


def get_best_player(gks):
    df = pd.DataFrame(gks, columns=["ID", "Position", "Name", "Club", "Points", "Price"])

    best_player = df.nlargest(2, ['Points']).values.tolist()

    return best_player[-1]

    pass


def local(players, W):
    lineup, profit, lineup_price = greedy_knapsack(players, W)
    print (profit)
    #print (np.array(lineup))
    print (lineup_price)

    all_players = remove_some_players(players, lineup)
    gks, mids, defs, fws = get_players_by_position(all_players)
    best_gk = get_best_player(gks)
    best_mid = get_best_player(mids)
    best_def = get_best_player(defs)
    best_fw = get_best_player(fws)

    susjedstvo = []
    for index, player in enumerate(lineup):
        pom_lineup = lineup.copy()


        if player[1] == 'MID':
            pom_lineup[index] = best_mid
        elif player[1] == 'GK':
            pom_lineup[index] = best_gk
        elif player[1] == 'DEF':
            pom_lineup[index] = best_def
        elif player[1] == 'FW':
            pom_lineup[index] = best_fw

        susjedstvo.append(pom_lineup)


    sve_cijene=[]
    for susjed in susjedstvo:
        prices = [x[5] for x in susjed]
        sve_cijene.append(sum(prices))

    print (sve_cijene)

    for index,cijena in enumerate(sve_cijene):
        if cijena>lineup_price and cijena<W:
            novi_lineup=susjedstvo[index]

    print (np.array(novi_lineup))


    dobit = [x[4] for x in novi_lineup]
    print (sum(dobit))





if __name__ == '__main__':
    lineup = []

    INITIAL_BUDGET = 100

    # read CSV
    df = pd.read_csv(PATH_TO_CSV, names=["ID", "Position", "Name", "Club", "Points", "Price"])

    worst_4 = pick_worst_4(df)
    lineup.extend(worst_4)

    # all players does not contain worst_4
    all_players = remove_some_players(df.values.tolist(), worst_4)
    # print (all_players)

    # eleven, profit, price = greedy_knapsack(all_players, W=INITIAL_BUDGET - money_spent(worst_4))
    # print (price)
    # print(profit)
    # print(np.array(eleven))

    # local_search(all_players,W=INITIAL_BUDGET - money_spent(worst_4))

    local(all_players, W=INITIAL_BUDGET - money_spent(worst_4))

import random
import pandas as pd
import numpy as np
from utils import *

PATH_TO_CSV_1 = './instances/instance1.csv'
PATH_TO_CSV_2 = './instances/instance2.csv'


def really_greedy(best_players, W, clubs_of_worst):
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
                position == 'DEF' and taken_positions.count('DEF') == 3) \
                or (position == 'MID' and taken_positions.count('MID') == 5) or (
                position == 'FW' and taken_positions.count('FW') == 2) \
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


def ppm_greedy(best_players, W, clubs_of_worst):
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
                position == 'DEF' and taken_positions.count('DEF') == 3) \
                or (position == 'MID' and taken_positions.count('MID') == 5) or (
                position == 'FW' and taken_positions.count('FW') == 2) \
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


def local_search(players, W, clubs_of_worst):
    lineup, profit, lineup_price = ppm_greedy(players, W, clubs_of_worst)

    all_players = remove_some_players(players, lineup)
    gks, mids, defs, fws = get_players_by_position(all_players)

    counter = 0
    postava = lineup.copy()
    while counter < 100000:
        new_lineup = postava.copy()

        random_index = random.randrange(len(postava))
        random_player = postava[random_index]

        clubs_from = []
        for i in postava:
            clubs_from.append(i[3])

        # zamijeni ga s random igracem iz te pozicije
        if random_player[1] == 'MID':
            random_mid = random.choice(mids)
            while (random_mid in postava) or (
                    clubs_from.count(random_mid[3]) + clubs_of_worst.count(random_mid[3])) == 3:
                random_mid = random.choice(mids)
            new_lineup[random_index] = random_mid

        elif random_player[1] == 'GK':
            random_gk = random.choice(gks)
            while random_gk in postava or (clubs_from.count(random_gk[3]) + clubs_of_worst.count(random_gk[3])) == 3:
                random_gk = random.choice(gks)
            new_lineup[random_index] = random_gk

        elif random_player[1] == 'DEF':
            random_def = random.choice(defs)
            while random_def in postava or (clubs_from.count(random_def[3]) + clubs_of_worst.count(random_def[3])) == 3:
                random_def = random.choice(defs)
                if clubs_from.count(random_def[3]) == 3:
                    continue

            new_lineup[random_index] = random_def
        elif random_player[1] == 'FW':
            random_fw = random.choice(fws)
            while random_fw in postava or (clubs_from.count(random_fw[3]) + clubs_of_worst.count(random_fw[3])) == 3:
                random_fw = random.choice(fws)
            new_lineup[random_index] = random_fw

        novi_profit = sum([x[4] for x in new_lineup])
        novi_trosak = sum([x[5] for x in new_lineup])

        # ako je ovo rjesenje bolje, stavi ga kao novi lineup
        if novi_profit > profit and novi_trosak <= W:
            postava = new_lineup
            profit = novi_profit
            lineup_price = novi_trosak

        counter += 1

    return postava, profit, lineup_price


if __name__ == '__main__':
    lineup = []

    INITIAL_BUDGET = 100

    # df = pd.read_csv(PATH_TO_CSV_1, names=["ID", "Position", "Name", "Club", "Points", "Price"])
    df = pd.read_csv(PATH_TO_CSV_2, names=["ID", "Position", "Name", "Club", "Points", "Price"])
    worst_4 = pick_worst_4(df)
    lineup.extend(worst_4)

    clubs_of_worst = []
    for player in worst_4:
        clubs_of_worst.append(player[3])

    players_left = remove_some_players(df.values.tolist(), worst_4)
    # eleven_picked, profit, price = really_greedy(players_left, INITIAL_BUDGET - money_spent(worst_4), clubs_of_worst)
    # eleven_picked, profit, price = ppm_greedy(players_left, INITIAL_BUDGET - money_spent(worst_4), clubs_of_worst)
    eleven_picked, profit, price = local_search(players_left, INITIAL_BUDGET - money_spent(worst_4), clubs_of_worst)

    lineup.extend(eleven_picked)

    print(np.array(lineup))
    print('Profit', profit)
    print('Price', price + money_spent(worst_4))

    write_to_txt('validator/result.txt', worst_4, eleven_picked)

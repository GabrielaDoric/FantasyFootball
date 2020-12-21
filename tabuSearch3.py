from utils import *

PATH_TO_CSV_1 = './instances/instance1.csv'
PATH_TO_CSV_2 = './instances/instance2.csv'
PATH_TO_CSV_3 = './instances/instance3.csv'


def generate_neighborhood(players, s, clubs_of_worst, W):
    neighborhood = []
    positions_replaced = []

    gks, mids, defs, fws = get_players_by_position(players)
    dicti = {'MID': mids, 'GK': gks, 'FW': fws, 'DEF': defs}

    num_of_neighbors = 10000
    while len(neighborhood) < num_of_neighbors:
        while True:

            index1, index2 = random.sample(range(0, 11), 2)
            player1 = s[index1]
            player2 = s[index2]

            # pick player with matching position
            random_index1 = random.randrange(len(dicti[player1[1]]))
            random_player1 = dicti[player1[1]][random_index1]

            random_index2 = random.randrange(len(dicti[player2[1]]))
            random_player2 = dicti[player2[1]][random_index2]

            if random_player1 in s or random_player2 in s:
                continue

            pom_lineup = s.copy()
            pom_lineup[index1] = random_player1
            pom_lineup[index2] = random_player2

            # ako je ovaj lineup vec u susjedstvu, continue
            if pom_lineup in neighborhood:
                continue

            # ako dodavanje ovog igraca narusava budzet, continue
            if get_money_spent(pom_lineup) > W:
                continue

            # check is addind first replacement violates rule 3 max from same team
            clubs_from = []
            for element in pom_lineup:
                clubs_from.append(element[3])
            if (clubs_from.count(random_player1[3]) + clubs_of_worst.count(random_player1[3]) > 3) \
                    or (clubs_from.count(random_player2[3]) + clubs_of_worst.count(random_player2[3]) > 3):
                continue

            positions_replaced.append(((player1[1], player2[1])))
            neighborhood.append(pom_lineup)
            break

    return neighborhood, positions_replaced


def get_best_neighbor(neighborhood, positions_replaced, tabu_list):
    best_profit = 0
    index_of_best = 0

    for i, neighbor in enumerate(neighborhood):
        pozicije = positions_replaced[i]
        for tabu in tabu_list:
            if set(pozicije) == set(tabu):
                continue

        profit = get_profit(neighbor)
        if profit > best_profit:
            best_profit = profit
            best_neighbor = neighbor
            index_of_best = i

    return best_neighbor, index_of_best


def tabu_search(players, W, clubs_of_worst, formation):
    lineup, profit, lineup_price = ppm_greedy(players, W, clubs_of_worst, formation)
    s = lineup.copy()
    s_best = lineup.copy()
    tabu_list = []

    iterations = 10
    for i in range(iterations):

        # get neighborhood
        neighborhood, positions_replaced = generate_neighborhood(players, s, clubs_of_worst, W)

        # get best neighbor
        s, s_index = get_best_neighbor(neighborhood, positions_replaced, tabu_list)

        # update tabu list
        dobre_pozicije = positions_replaced[s_index]
        if len(tabu_list) < 5:
            tabu_list.append((dobre_pozicije))
        else:
            del tabu_list[0]
            tabu_list.append(((dobre_pozicije)))

        # update best solution
        if get_profit(s) > get_profit(s_best):
            s_best = s

    return s_best, get_profit(s_best), get_money_spent(s_best)


if __name__ == '__main__':

    lineup = []
    INITIAL_BUDGET = 100

    #df = pd.read_csv(PATH_TO_CSV_1, names=["ID", "Position", "Name", "Club", "Points", "Price"])
    df = pd.read_csv(PATH_TO_CSV_2, names=["ID", "Position", "Name", "Club", "Points", "Price"])
    # df = pd.read_csv(PATH_TO_CSV_3, encoding='latin-1' ,names=["ID", "Position", "Name", "Club", "Points", "Price"])

    # formations = [[1, 1, 2, 0], [1, 0, 2, 1], [1, 2, 1, 0], [1, 0, 1, 2], [1, 3, 0, 0], [1, 2, 0, 1], [1, 1, 0, 2]]
    formations = [[1, 0, 2, 1]]
    # formations = [[1,3,0,0]]
    for formation in formations:
        lineup = []
        worst_4 = pick_worst_4(df, formation)
        lineup.extend(worst_4)

        clubs_of_worst = []
        for player in worst_4:
            clubs_of_worst.append(player[3])

        players_left = remove_some_players(df.values.tolist(), worst_4)

        eleven_picked, profit, price = tabu_search(players_left, INITIAL_BUDGET - money_spent(worst_4), clubs_of_worst,
                                                   formation)

        lineup.extend(eleven_picked)

        print(np.array(lineup))
        print('Profit', profit)
        print('Price', price + money_spent(worst_4))
        print('---------------------------------------------')

        write_to_txt('validator/result.txt', worst_4, eleven_picked)

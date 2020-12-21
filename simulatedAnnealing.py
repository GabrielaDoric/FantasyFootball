from utils import *
import math

PATH_TO_CSV_1 = './instances/instance1.csv'
PATH_TO_CSV_2 = './instances/instance2.csv'
PATH_TO_CSV_3 = './instances/instance3.csv'



def select_neighbor(players, lineup, W, clubs_of_worst):

    gks, mids, defs, fws = get_players_by_position(players)
    dict = {'MID': mids, 'GK': gks, 'FW': fws, 'DEF': defs}

    while True:

        random_index = random.randrange(len(lineup))
        random_player = lineup[random_index]
        random_id, random_pos, random_name, random_club1, random_points, random_price = random_player


        replacement_index = random.randrange(len(dict[random_pos]))
        replacement_player = dict[random_pos][replacement_index]


        new_lineup = lineup.copy()
        new_lineup[random_index] = replacement_player

        clubs_from = []
        for i in new_lineup:
            clubs_from.append(i[3])

        if replacement_player in lineup:
            continue

        if get_money_spent(new_lineup) > W:
            continue

        if (clubs_from.count(random_club1) + clubs_of_worst.count(random_club1) > 3):
            continue

        break
    return new_lineup


def SA(players, W, clubs_of_worst,formation):

    initial_lineup, profit, lineup_price = ppm_greedy(players, W, clubs_of_worst, formation)
    print('greedy profit', profit)

    initial_temperature = 100

    s = initial_lineup
    s_best = initial_lineup
    T = initial_temperature

    while (T > 0.01):

        for j in range(5):
            neighbor = select_neighbor(players, s, W, clubs_of_worst)
            if get_profit(neighbor) > get_profit(s):
                break

        delta_f = get_profit(s_best) - get_profit(neighbor)
        if delta_f<0:
            delta_f = 0

        if get_profit(neighbor)>get_profit(s):
            s = neighbor
        elif (get_profit(neighbor)<=get_profit(s)) and (random.uniform(0,1) < math.exp(-delta_f/T)):
            s = neighbor

        if get_profit(s) > get_profit(s_best):
            s_best = s

        T = T/(1+0.01*T)
        #T = T - 0.001
        #T = T*0.99


    return s_best, get_profit(s_best), get_money_spent(s_best)



if __name__ == '__main__':


    INITIAL_BUDGET = 100

    #df = pd.read_csv(PATH_TO_CSV_1, names=["ID", "Position", "Name", "Club", "Points", "Price"])
    #df = pd.read_csv(PATH_TO_CSV_2, names=["ID", "Position", "Name", "Club", "Points", "Price"])
    df = pd.read_csv(PATH_TO_CSV_3, encoding='latin-1' ,names=["ID", "Position", "Name", "Club", "Points", "Price"])

    formations = [[1, 1, 2, 0], [1, 0, 2, 1], [1, 2, 1, 0], [1, 0, 1, 2], [1, 3, 0, 0], [1, 2, 0, 1], [1, 1, 0, 2]]
    #formations = [[1, 2, 1, 0]]
    for formation in formations:
        lineup = []
        worst_4 = pick_worst_4(df, formation)
        lineup.extend(worst_4)

        clubs_of_worst = []
        for player in worst_4:
            clubs_of_worst.append(player[3])


        players_left = remove_some_players(df.values.tolist(), worst_4)

        eleven_picked, profit, price = SA(players_left, INITIAL_BUDGET - money_spent(worst_4), clubs_of_worst, formation)

        lineup.extend(eleven_picked)

        print(np.array(lineup))
        print('Profit', profit)
        print('Price', price + money_spent(worst_4))
        print('--------------------------------')

        write_to_txt('validator/result.txt', worst_4, eleven_picked)

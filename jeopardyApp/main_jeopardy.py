# Jeopardy home screen
import time
import sqlite3
import pickle
import random
import copy

from sqlite3 import Error


db_file = "/home/kyle/Documents/Python Projects/jeopardyGame/jeopardySite/clues.db"
pickle_file = "used_games.pkl"
pickled_game = "running_game.pkl"
#Connect to sqllite db
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        # sqlite3.enable_callback_tracebacks(True)
        conn = sqlite3.connect(db_file)


        return conn
    except Error as e:
        print(e)

    return None

def select_a_game(conn):
    """
    Query all games, checks against recently used games,
    returns the id of game to play
    """
    #selects all games and builds gamelist
    cur = conn.cursor()

    cur.execute("SELECT game FROM airdates")

    game_list = cur.fetchall()

    #gets used games
    used_list = get_pickled_games(pickle_file)

    #randomly selects a game that is not used and complere
    selected = False
    while not selected:
        #not in used games
        try_game =random.choice(game_list)
        try_game = int(try_game[0])
        if try_game not in used_list:

            game_data = get_game_data(conn, try_game)
            pickle_used_games(pickle_file, try_game) #add to used games
            #if complete game
            if len(game_data) ==61:
                selected = True
    return try_game, game_data

def get_game_data(conn , game_id):
    game_id = int(game_id)
    cur = conn.cursor()
    cur.execute("SELECT clues.id, game, round, value, clue, answer FROM clues JOIN documents ON clues.id = documents.id")
    whole_list = cur.fetchall()

    game_list = []
    #find our game items
    for i in whole_list:
        if i[1]==game_id:
            game_list.append(i)
    return game_list

def parse_game_data(game_list):

    #get game date
    #write the sql query here lol

    #1st round
    round_1_clues = []

    for i in game_list:
        if int(i[2]) == 1:
            try:
                q_info = []
                quest, answer, points = i[4],i[5],i[3]
                q_info.extend((quest,answer,points))
            except IndexError:
                print "NO FULL LIST", i
            #get catagory
            conn = create_connection(db_file)
            cur = conn.cursor()
            cur.execute("SELECT clue_id, category FROM classifications JOIN categories ON category_id = categories.id WHERE clue_id = ?", (i[0],))
            cat = cur.fetchall()
            cat = cat[0][1]
            q_info.append(cat)
            round_1_clues.append(q_info)

            #now build a dict to interact
            round_1_dict = {}
            for i in round_1_clues:
                try:
                    round_1_dict[i[3]].append(i[:3])
                except KeyError:
                    round_1_dict[i[3]] = [i[:3]]

    #second round
    round_2_clues = []
    for i in game_list:
        if int(i[2]) == 2:
            try:
                q_info = []
                quest, answer, points = i[4],i[5],i[3]
                q_info.extend((quest,answer,points))
            except IndexError:
                print "NO FULL LIST", i
            #get catagory
            conn = create_connection(db_file)
            cur = conn.cursor()
            cur.execute("SELECT clue_id, category FROM classifications JOIN categories ON category_id = categories.id WHERE clue_id = ?", (i[0],))
            cat = cur.fetchall()
            cat = cat[0][1]
            q_info.append(cat)
            round_2_clues.append(q_info)

            #now build a dict to interact
            round_2_dict = {}
            for i in round_2_clues:
                try:
                    round_2_dict[i[3]].append(i[:3])
                except KeyError:
                    round_2_dict[i[3]] = [i[:3]]
    #final jeopardy
    final_dict ={}
    round_3_clues = []
    for i in game_list:
        if int(i[2]) == 3:
            try:
                q_info = []
                quest, answer, points = i[4],i[5],i[3]
                q_info.extend((quest,answer,points))
            except IndexError:
                print "NO FULL LIST", i
            #get catagory
            conn = create_connection(db_file)
            cur = conn.cursor()
            cur.execute("SELECT clue_id, category FROM classifications JOIN categories ON category_id = categories.id WHERE clue_id = ?", (i[0],))
            cat = cur.fetchall()
            cat = cat[0][1]
            q_info.append(cat)
            round_3_clues.append(q_info)

            #now build a dict to interact
            for i in round_3_clues:
                try:
                    final_dict[i[3]].append(i[:3])
                except KeyError:
                    final_dict[i[3]] = [i[:3]]

    full_list = [round_1_dict, round_2_dict, final_dict]
    return remove_daily_doubles(full_list)

def remove_daily_doubles(game_dict):

    for i in game_dict[0:1]:
        for categories in i:
            counting = 1
            for q in i[categories]:
                q[2] = counting
                counting+=1
    return game_dict





def get_pickled_games(pickle_file):
    #gets a list of used games
    try:
        with open(pickle_file,'rb') as f:
            used_list = pickle.load(f)
    except:
        print "No file"
        used_list = []
    return used_list

def pickle_used_games(pickle_file, game_num):
    #used to pickle a recently used game
    used = get_pickled_games(pickle_file)
    with open(pickle_file, 'wb') as f:
        used.append(game_num)
        pickle.dump(used,f)
    return

def clear_pickled_games(pickle_file):
    #clears the file of used game
    with open(pickle_file, 'wb') as f:
        pickle.dump([],f)
    print "pickle cleared"
    return

def start_game():
    conn = create_connection(db_file)
    try_game, game_data = select_a_game(conn)
    game_dict = parse_game_data(game_data)

    return game_dict

def start_game_data_re(round):
    round = round -1
    if round == 0:
        conn = create_connection(db_file)
        try_game, game_data = select_a_game(conn)
        game_dict = parse_game_data(game_data)
        pickle_game_dict(pickled_game, game_dict)
        game_list= []
        cat_list = []
        for i in game_dict[round]:
            cat_list.append(i)
        game_list.append(cat_list)
        for i in game_dict[round]:
            cater = []
            for i in game_dict[round][i]:
                cater.append((i[0],i[1]))
            game_list.append(cater)



        #
        return game_list
    if round == 1:
        try:
             game_dict = get_pickled_game(pickled_game)
        except:
            start_game_data_re(1)
            game_dict = get_picked_game(pickled_game)

        game_list= []
        cat_list = []
        for i in game_dict[round]:
            cat_list.append(i)
        game_list.append(cat_list)
        for i in game_dict[round]:
            cater = []
            for i in game_dict[round][i]:
                cater.append((i[0],i[1]))
            game_list.append(cater)
        return game_list
    if round == 2:
        try:
             game_dict = get_pickled_game(pickled_game)

        except:
            start_game_data_re(1)
            game_dict = get_picked_game(pickled_game)

        final_q = game_dict[2]
        game_list =[]
        cat_list=[]
        for i in final_q:
            cat_list.append(i)
        game_list.append(cat_list)
        for i in final_q:
            cater = []
            for i in game_dict[round][i]:
                cater.append((i[0],i[1]))
            game_list.append(cater)
        return game_list



def pickle_game_dict(pickled_game, game_dict):
    with open(pickled_game, 'wb') as f:
        pickle.dump(game_dict,f)
    return

def get_pickled_game(pickled_game):
    with open(pickled_game, 'rb') as f:
        game_dict = pickle.load(f)
    return game_dict

def print_game(game_dict):
    ### change font using dconfig, org, gnome, desktop, interface, monospace font
    print "Loading game......"
    game = copy.deepcopy(game_dict)
    print
    print "Welcome to Jeopardy!"
    print

    #############ROUND1
    time.sleep(2)
    print "Let's start round 1"

    category_list = []
    counter = 0

    counter = 0
    while counter < 20:
        print
        print "Here are the categories!"
        print
        counter_1 = 0
        category_list = []
        for i in game[0]:
            counter_1+=1
            category_list.append(i)
            print counter_1, "--",i
            print
        print "Choose a category: (#)"
        category = 100
        while category not in [0,1,2,3,4,5]:
            try:
                category = int(raw_input()) -1
            except:
                pass
                # print "try again"
        time.sleep(1)
        items_left = []
        for i in game[0][category_list[category]]:
            items_left.append(i[2])
        if len(items_left) ==0:
            print "Pick a new category--that one is empty"
            continue
        print "Choose a value from "+str(items_left)
        value = 100
        while value not in items_left:
            try:
                value = int(raw_input())
            except:
                pass
            # print "try_again"
        time.sleep(2)
        print

        print "The clue:"
        print

        for i in game[0][category_list[category]]:
            if i[2] == value:
                question = i
        print "###########################"
        print question[0]
        print "###########################"
        time.sleep(6)
        print "3"
        print
        time.sleep(1)
        print "2"
        print
        time.sleep(1)
        print "1"
        print
        time.sleep(1)
        yes_or_no = 0
        print "Would you like to see the answer? (1)"
        print
        while yes_or_no != 1:
            yes_or_no = int(raw_input())
        print
        print "WHAT IS..."
        print "****************"
        print str(question[1])
        print "****************"
        print
        time.sleep(2)
        print "Good work!"
        counter+=1
        if counter != 20:
            print "Let's pick another question!"
        game[0][category_list[category]].remove(question)


    #############round_2
    print "~~~~~~~~~~~~~~~~~~~~~~"
    print "~~~~~~~~~~~~~~~~~~~~~~"
    print "Welcome to Double Jeopardy!"
    time.sleep(2)

    category_list = []
    counter = 0

    counter = 0
    while counter < 20:
        print
        print "Here are the categories!"
        print
        counter_1 = 0
        category_list = []
        for i in game[1]:
            counter_1+=1
            category_list.append(i)
            print counter_1, "--",i
            print
        print "Choose a category: (#)"
        category = 100
        while category not in [0,1,2,3,4,5]:
            try:
                category = int(raw_input()) -1
            except:
                pass
                # print "try again"
        time.sleep(1)
        items_left = []
        for i in game[1][category_list[category]]:
            items_left.append(i[2])
        if len(items_left) ==0:
            print "Pick a new category--that one is empty"
            continue
        print "Choose a value from "+str(items_left)
        value = 1
        while value not in items_left:
            try:
                value = int(raw_input())
            except:
                pass
            # print "try again"
        time.sleep(2)
        print
        print "The clue:"
        print

        for i in game[1][category_list[category]]:
            if i[2] == value:
                question = i
        print "###########################"
        print question[0]
        print "###########################"
        time.sleep(6)
        print "3"
        print
        time.sleep(1)
        print "2"
        print
        time.sleep(1)
        print "1"
        print
        time.sleep(1)
        yes_or_no = 0
        print "Would you like to see the answer? (1)"
        print
        while yes_or_no != 1:
            yes_or_no = int(raw_input())
        print
        print "WHAT IS..."
        print "****************"
        print str(question[1])
        print "****************"
        print
        time.sleep(2)
        print "Good work!"
        counter+=1
        if counter != 20:
            print "Let's pick another question!"
        game[1][category_list[category]].remove(question)

    print "~~~~~~~~~~~~~~~~~~~~~~"
    print "~~~~~~~~~~~~~~~~~~~~~~"
    print "Welcome to Final Jeopardy!"
    time.sleep(2)
    print "First, the category:"
    print
    for i in game[2]:
        print "@@@@@@@@@@@@@@@@@@@@"
        category = i
        print i
        print "@@@@@@@@@@@@@@@@@@@@"
    time.sleep(2)

    print "The clue:"
    print
    print "******************"
    print str(game[2][category][0][0])
    print "******************"
    ready = 0
    print "Type *1* when you are ready to see the answer!"
    while ready != 1:
        try:
            ready = int(raw_input())
        except:
            pass
    print
    print
    print "The answer is:"
    print
    print "**************************"
    print str(game[2][category][0][1])
    print "**************************"
    print
    print "Game Over"

"""
console controller
"""
import model as m


def list_of_markets(curs):
    """show list of markets"""
    markets = m.list_markets(curs)
    for market in markets:
        print('"'+market[0]+'"' + ' ID of market: ' + market[1])


def all_cities(curs):
    """shoe list of city"""
    cities = m.all_cities(curs)
    for city in cities:
        print(city)


def find_by(curs):
    """command for the searching markets"""
    print("The search is possible by city and state or by ZIP code")
    search_by = input("Select the command:\n1 - by city and state\n2 - by ZIP code"
                      "\nInput your command => ")
    if search_by == '1':
        name_of_city = input("Input name city ")
        name_of_state = input("Input name state ")
        markets = m.find_by_city(curs, name_of_city, name_of_state)
        if len(markets) > 1:
            for market in markets:
                print(market[0])
        else:
            print("invalid command")

    elif search_by == '2':
        zip_code = input("Input zip code ")
        market = m.find_by_zip(curs, zip_code)
        if market is None:
            print("Market not found")
        else:
            print(market)
    else:
        print("invalid command")


def details_of_market(curs):
    """show details about market"""
    market = input("Input name of market => ")
    details = m.detailed_data(curs, market)
    if len(details) > 1:
        print(f"found {len(details)} markets")
        for found_market in details:
            print(f"ID of market: {found_market[7]}")
            print(f"street: {found_market[0]}")
            print(f"City: {found_market[8]}")
            print(f"County: {found_market[9]}")
            print(f"State: {found_market[10]}")
            print(f"zip code: {found_market[4]}")
            print("media: ")
            for i in found_market[11:16]:
                if len(i) > 0:
                    print(i)
            print(f"coordinates: X = {found_market[5]} Y = {found_market[6]}")
    elif len(details) == 0:
        print("No markets found")
        cmd = input("Do you want to see the available stores?\n1 - Yes\n2 - No"
                    "\nInput your command => ")
        if cmd == '1':
            list_of_markets(curs)
    else:
        print(f"found {len(details)} markets")
        print(f"ID of market: {details[0][7]}")
        print(f"street: {details[0][0]}")
        print(f"City: {details[0][8]}")
        print(f"County: {details[0][9]}")
        print(f"State: {details[0][10]}")
        print(f"zip code: {details[0][4]}")
        print("media: ")
        for i in details[0][11:16]:
            if len(i) > 0:
                print(i)
        print(f"coordinates: X = {details[0][5]} Y = {details[0][6]}")


def review(curs, conn):
    """show and added review"""
    cmd = input("if you want to see reviews enter 1\nif you want to leave a review enter 2"
                "\nInput your command => ")
    if cmd == '1':
        id_market = input("(All ID of markets you can see by the command list, "
                          "if you want to see all ids enter 1)"
                          "\nInput ID of market => ")
        if id_market == '1':
            markets = m.list_markets(curs)
            for market in markets:
                print('"' + market[0] + '"' + ' ID of market: ' + market[1])
        else:
            comments = m.comm_market(curs, id_market)
            for comm in comments:
                print(comm)
    elif cmd == '2':
        id_market = input("(All ID of markets you can see by the command list, "
                          "if you want to see all ids enter 1)"
                          "\nInput ID of market => ")
        if id_market == '1':
            markets = m.list_markets(curs)
            for market in markets:
                print('"' + market[0] + '"' + ' ID of market: ' + market[1])
        else:
            cmmnt = input("Input your review => ")
            m.comments(curs, conn, cmmnt, id_market)
            print("Your comment is added")
    else:
        print("invalid command")


def rating(curs, conn):
    """show and added rating"""
    cmd = input("if you want to see rating enter 1\nif you want to leave a rating enter 2"
                "\nInput your command => ")
    if cmd == '1':
        id_market = input("(All ID of markets you can see by the command list, "
                          "if you want to see all ID enter list)"
                          "\nInput ID of market => ")
        if id_market == 'list':
            markets = m.list_markets(curs)
            for market in markets:
                print('"' + market[0] + '"' + ' ID of market: ' + market[1])
        else:
            ratings = m.rating_market(curs, id_market)
            if ratings[0][0] is None:
                print("the market does not have a rating yet\nor there is no such market")
            else:
                for rat in ratings:
                    print(rat)
    elif cmd == '2':
        id_market = input("(All ID of markets you can see by the command list, "
                          "if you want to see all ids enter list)"
                          "\nInput ID of market => ")
        if id_market == 'list':
            markets = m.list_markets(curs)
            for market in markets:
                print('"' + market[0] + '"' + ' ID of market: ' + market[1])
        else:
            rat = input("Input your rating => ")
            m.rating(curs, conn, rat, id_market)
            print("Your rating is added")
    else:
        print("invalid command")


def distance(curs):
    """show distance between markets or coordinates"""
    cmd = input("If you want to see distance between markets, input 1"
                "\nif you want to see distance between coordinates, input 2"
                "\nInput ID of market => ")
    if cmd == '1':
        first_market = input("(All ID of markets you can see by the command list, "
                             "if you want to see all ID enter list)"
                             "\nInput ID first market => ")
        if first_market == 'list':
            markets = m.list_markets(curs)
            for market in markets:
                print(f"'{market[0]}' ID of market: {market[1]}")
        else:
            second_market = input("Input ID second market => ")
            try:
                dist = m.dist_btwn_m(curs, first_market, second_market)
                print(f"distance between markets = {round(dist, 2)} miles")
            except TypeError:
                print("Incorrectly specified ID"
                      "\nYou can see all ID of markets by the command list of markets")
    elif cmd == '2':
        first_la = float(input("input latitude first market (Y) => "))
        first_lo = float(input("input longitude first market (X) => "))
        second_la = float(input("input latitude second market (Y) => "))
        second_lo = float(input("input longitude second market (X) => "))
        dist = m.distance(first_la, first_lo, second_la, second_lo)
        print(f"distance between markets = {round(dist, 2)} miles")
    else:
        print("invalid command")


def repl(curs, conn):
    """main"""
    cmd = 1
    while cmd == 1:
        cmd_list = ('1', '2', '3', '4', '5', '6', '7', '8')
        command = input("Select the command:\n1 - list of markets\n2 - all cities\n3 - find"
                        "\n4 - show details\n5 - review\n6 - rating\n7 - distance\n8 - end "
                        "\nInput your command => ")
        if command == cmd_list[0]:
            list_of_markets(curs)
        elif command == cmd_list[1]:
            all_cities(curs)
        elif command == cmd_list[2]:
            find_by(curs)
        elif command == cmd_list[3]:
            details_of_market(curs)
        elif command == cmd_list[4]:
            review(curs, conn)
        elif command == cmd_list[5]:
            rating(curs, conn)
        elif command == cmd_list[6]:
            distance(curs)
        elif command == cmd_list[7]:
            print("Good bay, friend!")
            cmd = 2
        else:
            print("there is no such command, try again")


if __name__ == '__main__':
    db_conn, db_curs = m.init('server.db')
    repl(db_curs, db_conn)
    m.close(db_conn, db_curs)

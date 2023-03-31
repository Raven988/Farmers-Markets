"""

DATA BASE SQLite3
Class Model
В качестве экземпляра класса выступает база данных

"""
import sqlite3
from math import radians, cos, sin, asin, sqrt


class Model:
    """The database acts as an instance of the class"""
    def __init__(self, f_name):            # Подключение к базе данных
        """init"""
        self.db_conn = sqlite3.connect(f_name)
        self.db_curs = self.db_conn.cursor()

    def close_conn(self):            # Закрытие базы данных
        """close connect"""
        self.db_curs.close()
        self.db_conn.close()

    def list_markets(self):          # Список всех рынков
        """select all name of market"""
        markets_list = []
        self.db_curs.execute("SELECT Name, ID FROM Markets")

        for result in self.db_curs:
            markets_list.append(f"{result[0]} - {result[1]}")
        return markets_list

    def all_cities(self):            # Список всех городов рынков
        """select all cities"""
        cities_list = []
        self.db_curs.execute("SELECT city FROM Cities ORDER BY city")
        for result in self.db_curs:
            cities_list.append(result[0])
        return cities_list

    def all_state(self):            # Список всех штатов рынков
        """select all states"""
        states_list = []
        self.db_curs.execute("SELECT state FROM States")
        for result in self.db_curs:
            states_list.append(result[0])
        return states_list

    def find_by_zip(self, zip_code):         # Поиск рынка по ZIP-коду
        """searching name of Market by ZIP code"""
        self.db_curs.execute("""SELECT idMarket FROM Addresses WHERE ZIP = ?""", (zip_code, ))
        id_fms = self.db_curs.fetchall()
        name_by_zip = []
        for name_fm in id_fms:
            self.db_curs.execute("""SELECT * FROM Markets WHERE ID = ?""", (name_fm[0],))
            name_by_zip.append(self.db_curs.fetchone())
        return name_by_zip

    def find_by_city(self, city, state):         # Поиск рынка по городу и штату
        """searching name of Market by city and state"""
        id_market = []
        self.db_curs.execute("""SELECT idMarket FROM Addresses WHERE City =
        (SELECT ID FROM Cities WHERE City = ?) AND State =
        (SELECT ID FROM States WHERE State = ?)""", (city, state))
        for result in self.db_curs:
            id_market.append(result)
        list_by = []
        for market in id_market:
            self.db_curs.execute("""SELECT Name FROM Markets WHERE ID = ? """, market)
            list_by.append(self.db_curs.fetchone())

        return list_by

    def detailed_data(self, id_market):            # Детали о рынке
        """shows details about Market"""
        found_street = []
        self.db_curs.execute(f"""SELECT City FROM Addresses
                        WHERE idMarket = {id_market}""")
        city = self.db_curs.fetchone()
        self.db_curs.execute(f"""SELECT State FROM Addresses
                        WHERE idMarket = {id_market}""")
        state = self.db_curs.fetchone()
        self.db_curs.execute(f"""SELECT County FROM Addresses
                        WHERE idMarket = {id_market}""")
        county = self.db_curs.fetchone()

        self.db_curs.execute(f"""SELECT addresses.*, cities.city, states.state,
        counties.county, media.*, markets.name FROM Addresses, Cities, states, counties,
        media, markets WHERE addresses.idmarket = {id_market} and cities.id = {city[0]}
        AND states.id = {state[0]} AND counties.id = {county[0]} AND markets.id = {id_market}
        AND media.idMarket = {id_market}""")
        found_street.append(self.db_curs.fetchone())

        return found_street

    def comments(self, comment, id_market):     # Добавление комментария в БД
        """Adding a comment to market"""
        self.db_curs.execute("""INSERT INTO Comments VALUES (?,?)""", (comment, id_market))
        self.db_conn.commit()

    def rating(self, rating_m, id_market):   # Добавление рейтинга в БД
        """Adding a rating to market"""
        self.db_curs.execute("""INSERT INTO Ratings VALUES (?,?)""", (rating_m, id_market))
        self.db_conn.commit()

    def dist_btwn_m(self, market1, market2):     # расчет дистанции между рынками
        """determining the distance between markets"""
        self.db_curs.execute("""SELECT LocX, LocY FROM Addresses WHERE
        idMarket = """, (market1, ))
        mrkt1 = self.db_curs.fetchone()
        self.db_curs.execute("""SELECT LocX, LocY FROM Addresses WHERE
        idMarket = """, (market2, ))
        mrkt2 = self.db_curs.fetchone()
        lon1 = radians(float(mrkt1[0]))
        lon2 = radians(float(mrkt2[0]))
        lat1 = radians(float(mrkt1[1]))
        lat2 = radians(float(mrkt2[1]))
        d_lo = lon2 - lon1
        d_la = lat2 - lat1
        d_p = sin(d_la / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lo / 2) ** 2
        result = ((2 * asin(sqrt(d_p))) * 3959)
        return result

    def comm_market(self, id_market):         # коммнтарии магазина
        """add comments about the market"""
        cmnts = []
        self.db_curs.execute("""SELECT Comment FROM Comments WHERE idMarket = ?""", (id_market,))
        for comment in self.db_curs:
            cmnts.append(comment)
        return cmnts

    def rating_market(self, idmarket):         # средний рейтинг магазина
        """add rating about the market"""
        self.db_curs.execute("""SELECT AVG(Rating) FROM Ratings WHERE idMarket = ?""", (idmarket, ))
        rating = self.db_curs.fetchall()
        return rating

    def all_id(self):
        """select all ID from DB"""
        self.db_curs.execute("""SELECT ID FROM Markets""")
        id_fm = self.db_curs.fetchall()
        return id_fm

    def all_zip(self):
        """select all ZIP from DB"""
        self.db_curs.execute("""SELECT ZIP FROM Addresses""")
        all_zip_fm = self.db_curs.fetchall()
        return all_zip_fm

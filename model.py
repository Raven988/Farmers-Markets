"""

DATA BASE SQLite3
Model

"""
import sqlite3
import csv
from math import radians, cos, sin, asin, sqrt


# region BLOCK #1 ETL
def etl(connect, cursor, file_csv):         # Создание базы данных
    """creating table"""
    data = []
    with open(file_csv, 'r', encoding="utf-8") as f_in:
        reader = csv.reader(f_in)
        for row in reader:
            row_list = []
            for i in row:
                row_list.append(i.strip())
            data.append(row_list)

    create_csv = """CREATE TABLE IF NOT EXISTS Marketscsv (
    FMID TEXT, MarketName TEXT, Website	TEXT, Facebook TEXT, 
    Twitter TEXT, Youtube TEXT, OtherMedia TEXT, street	TEXT, 
    city TEXT, County TEXT, State TEXT, zip	TEXT, Season1Date TEXT, 
    Season1Time TEXT, Season2Date TEXT, Season2Time	TEXT, 
    Season3Date TEXT, Season3Time TEXT, Season4Date	TEXT, 
    Season4Time	TEXT, x	TEXT, y	TEXT, Location	TEXT, 
    Credit TEXT, WIC TEXT, WICcash TEXT, SFMNP TEXT, SNAP TEXT, 
    Organic	TEXT, Bakedgoods TEXT, Cheese TEXT, Crafts	TEXT, 
    Flowers	TEXT, Eggs TEXT, Seafood TEXT, Herbs TEXT, 
    Vegetables TEXT, Honey TEXT, Jams TEXT, Maple	TEXT, 
    Meat TEXT, Nursery TEXT, Nuts TEXT, Plants TEXT, 
    Poultry TEXT, Prepared TEXT, Soap TEXT, Trees TEXT,
    Wine TEXT, Coffee TEXT, Beans TEXT, Fruits TEXT, 
    Grains TEXT, Juices TEXT, Mushrooms TEXT, PetFood TEXT, 
    Tofu TEXT, WildHarvested TEXT, updateTime TEXT)"""
    cursor.executescript(create_csv)

    cursor.executemany("""INSERT INTO Marketscsv VALUES (?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", data[1:])

    create_table = """
    CREATE TABLE IF NOT EXISTS `Markets` (
    `ID` VARCHAR(255) NOT NULL PRIMARY KEY,
    `Name` VARCHAR(255),
    `UpdateTime` VARCHAR(255));

    CREATE TABLE IF NOT EXISTS `Addresses` (
    `Street` VARCHAR(255),      `City` INT,
    `County` INT,               `State` INT,
    `ZIP` INT,                  `LocX` VARCHAR(45),
    `LocY` VARCHAR(45),         `idMarket` INT NOT NULL,
    FOREIGN KEY (`idMarket`) REFERENCES `Markets` (`ID`),
    FOREIGN KEY (`City`) REFERENCES `Cities` (`ID`),
    FOREIGN KEY (`County`) REFERENCES `Counties` (`ID`),
    FOREIGN KEY (`State`) REFERENCES `States` (`ID`));

    CREATE TABLE IF NOT EXISTS `Media` (
    `Website` VARCHAR(255) NULL,    `Facebook` VARCHAR(255) NULL,
    `Twitter` VARCHAR(255) NULL,    `Youtube` VARCHAR(255) NULL,
    `OtherMedia` VARCHAR(255) NULL, `idMarket` INT NOT NULL,
    FOREIGN KEY (`idMarket`) REFERENCES `Markets` (`ID`));

    CREATE TABLE IF NOT EXISTS `Cities` (
    `ID` INTEGER NOT NULL PRIMARY KEY,
    `City` VARCHAR(255));

    CREATE TABLE IF NOT EXISTS `Counties` (
    `ID` INTEGER NOT NULL PRIMARY KEY,
    `County` VARCHAR(45));

    CREATE TABLE IF NOT EXISTS `States` (
    `ID` INTEGER NOT NULL PRIMARY KEY,
    `State` VARCHAR(45));

    CREATE TABLE IF NOT EXISTS `Comments` (
    `Comment` TEXT NOT NULL,
    `idMarket` INT NOT NULL,
    FOREIGN KEY (`idMarket`) REFERENCES `Markets` (`ID`));

    CREATE TABLE IF NOT EXISTS `Ratings` (
    `Rating` INT NOT NULL,
    `idMarket` INT NOT NULL,
    FOREIGN KEY (`idMarket`) REFERENCES `Markets` (`ID`));

    CREATE TABLE IF NOT EXISTS `Seasons` (
    `Season1Date` VARCHAR(45),        `Season1Time` VARCHAR(45),
    `Season2Date` VARCHAR(45),        `Season2Time` VARCHAR(45),
    `Season3Date` VARCHAR(45),        `Season3Time` VARCHAR(45),
    `Season4Date` VARCHAR(45),        `Season4Time` VARCHAR(45),
    `idMarket` INT NOT NULL,
      FOREIGN KEY (`idMarket`) REFERENCES `Markets` (`ID`));

    CREATE TABLE IF NOT EXISTS `PaymentMethods` (
    `Credit` VARCHAR(45),          `WIC` VARCHAR(45),
    `WICcash` VARCHAR(45),         `SFMNP` VARCHAR(45),
    `SNAP` VARCHAR(45),            `idMarket` INT NOT NULL,
      FOREIGN KEY (`idMarket`) REFERENCES `Markets` (`ID`));

    CREATE TABLE IF NOT EXISTS `Categories` (
    `Organic` VARCHAR(45),             `Bakedgoods` VARCHAR(45),
    `Cheese` VARCHAR(45),              `Crafts` VARCHAR(45),
    `Flowers` VARCHAR(45),             `Eggs` VARCHAR(45),
    `Seafood` VARCHAR(45),             `Herbs` VARCHAR(45),
    `Vegetables` VARCHAR(45),          `Honey` VARCHAR(45),
    `Jams` VARCHAR(45),                `Maple` VARCHAR(45),
    `Meat` VARCHAR(45),                `Nursery` VARCHAR(45),
    `Nuts` VARCHAR(45),                `Plants` VARCHAR(45),
    `Poultry` VARCHAR(45),             `Prepared` VARCHAR(45),
    `Soap` VARCHAR(45),                `Trees` VARCHAR(45),
    `Wine` VARCHAR(45),                `Coffee` VARCHAR(45),
    `Beans` VARCHAR(45),               `Fruits` VARCHAR(45),
    `Grains` VARCHAR(45),              `Juices` VARCHAR(45),
    `Mushrooms` VARCHAR(45),           `PetFood` VARCHAR(45),
    `Tofu` VARCHAR(45),                `WildHarvested` VARCHAR(45),
    `idMarket` INT NOT NULL,
      FOREIGN KEY (`idMarket`) REFERENCES `Markets` (`ID`))"""
    cursor.executescript(create_table)

    insertscript = """
    INSERT INTO Markets (ID, Name) SELECT FMID, MarketName
    FROM Marketscsv;

    INSERT INTO Addresses (Street, ZIP, LocX, LocY, idMarket)
    SELECT Street, ZIP, X, Y, FMID FROM Marketscsv;

    INSERT INTO Media SELECT Website, Facebook, Twitter,
     Youtube, OtherMedia, FMID FROM Marketscsv;

    INSERT INTO Seasons SELECT Season1Date, Season1Time,
    Season2Date, Season2Time, Season3Date, Season3Time,
    Season4Date, Season4Time, FMID FROM Marketscsv;

    INSERT INTO PaymentMethods SELECT Credit, WIC, WICcash,
    SFMNP, SNAP, FMID FROM Marketscsv;

    INSERT INTO Categories SELECT Organic, Bakedgoods, Cheese,
    Crafts, Flowers, Eggs, Seafood, Herbs, Vegetables, Honey,
    Jams, Maple, Meat, Nursery, Nuts, Plants, Poultry, Prepared,
    Soap, Trees, Wine, Coffee, Beans, Fruits, Grains, Juices,
    Mushrooms, PetFood, Tofu, WildHarvested, FMID FROM Marketscsv;

    INSERT INTO Cities (City) SELECT DISTINCT City FROM Marketscsv;
    INSERT INTO Counties (County) SELECT DISTINCT County FROM Marketscsv;
    INSERT INTO States (state) SELECT DISTINCT state FROM Marketscsv"""
    cursor.executescript(insertscript)
    connect.commit()


def insert_city(connect, cursor):
    """inserting cities in table"""
    cursor.execute("""SELECT City FROM Marketscsv""")
    city_from_csv = cursor.fetchall()
    cursor.execute("SELECT * FROM Cities")
    city_from_cities = cursor.fetchall()
    in_t1 = []
    for i in city_from_csv:
        for j in city_from_cities:
            if i[0] in j:
                in_t1.append(j[0])
    rowid1 = 1
    for i in in_t1:
        cursor.execute("""UPDATE Addresses SET City = ? WHERE rowid = ?""", (i, rowid1))
        rowid1 += 1
    connect.commit()


def insert_county(connect, cursor):
    """inserting counties in table"""
    cursor.execute("""SELECT county FROM Marketscsv""")
    county_from_csv = cursor.fetchall()
    cursor.execute("SELECT * FROM Counties")
    county_from_counties = cursor.fetchall()
    in_t2 = []
    for i in county_from_csv:
        for j in county_from_counties:
            if i[0] in j:
                in_t2.append(j[0])
    rowid2 = 1
    for i in in_t2:
        cursor.execute("""UPDATE Addresses SET County = ? WHERE rowid = ?""", (i, rowid2))
        rowid2 += 1
    connect.commit()


def insert_state(connect, cursor):
    """inserting states in table"""
    cursor.execute("""SELECT state FROM Marketscsv""")
    state_from_csv = cursor.fetchall()
    cursor.execute("SELECT * FROM States")
    state_from_states = cursor.fetchall()
    in_t3 = []
    for i in state_from_csv:
        for j in state_from_states:
            if i[0] in j:
                in_t3.append(j[0])
    rowid3 = 1
    for i in in_t3:
        cursor.execute("""UPDATE Addresses SET State = ? WHERE rowid = ?""", (i, rowid3))
        rowid3 += 1
    connect.commit()


# endregion
# region BLOCK #2 Model


def init(f_name):            # Подключение к базе данных
    """init"""
    db_conn = sqlite3.connect(f_name)
    db_curs = db_conn.cursor()
    return db_conn, db_curs


def close(db_conn, db_curs):            # Закрытие базы данных
    """close connect"""
    db_curs.close()
    db_conn.close()


def list_markets(db_curs):          # Список всех рынков
    """select all name of market"""
    markets_list = []
    db_curs.execute("SELECT Name, ID FROM Markets")
    for result in db_curs:
        markets_list.append(result)
    return markets_list


def all_cities(db_curs):            # Список всех городов рынков
    """select all cities"""
    cities_list = []
    db_curs.execute("SELECT city FROM Cities ORDER BY city")
    for result in db_curs:
        cities_list.append(result[0])
    return cities_list


def find_by_zip(db_curs, zip_code):         # Поиск рынка по ZIP-коду
    """searching name of Market by ZIP code"""
    db_curs.execute("""SELECT Name FROM Markets WHERE
    ID = (SELECT idMarket FROM Addresses WHERE ZIP = ?)""", (zip_code, ))
    name_by_zip = db_curs.fetchone()
    return name_by_zip


def find_by_city(db_curs, city, state):         # Поиск рынка по городу и штату
    """searching name of Market by city and state"""
    id_market = []
    db_curs.execute("""SELECT idMarket FROM Addresses WHERE City =
    (SELECT ID FROM Cities WHERE City = ?) AND State =
    (SELECT ID FROM States WHERE State = ?)""", (city, state))
    for result in db_curs:
        id_market.append(result)
    list_by = []
    for i in id_market:
        db_curs.execute("""SELECT Name FROM Markets WHERE ID = ? """, i)
        list_by.append(db_curs.fetchone())

    return list_by


def detailed_data(db_curs, name_market):            # Детали о рынке
    """shows details about Market"""
    found_id = []
    db_curs.execute("""SELECT ID FROM Markets WHERE Name = ? """,
                    (name_market, ))
    for result in db_curs:
        found_id.append(result)
    found_street = []
    for i in found_id:
        db_curs.execute(f"""SELECT City FROM Addresses
                        WHERE idMarket = {i[0]}""")
        city = db_curs.fetchone()
        db_curs.execute(f"""SELECT State FROM Addresses
                        WHERE idMarket = {i[0]}""")
        state = db_curs.fetchone()
        db_curs.execute(f"""SELECT County FROM Addresses
                        WHERE idMarket = {i[0]}""")
        county = db_curs.fetchone()

        db_curs.execute(f"""SELECT addresses.*, cities.city, states.state,
        counties.county, media.* FROM Addresses, Cities, states, counties,
        media WHERE addresses.idmarket = {i[0]} and cities.id = {city[0]}
        AND states.id = {state[0]} AND counties.id = {county[0]}
        AND media.idMarket = {i[0]}""")
        found_street.append(db_curs.fetchone())

    return found_street


def comments(db_curs, db_conn, comment, id_market):     # Добавление комментария в БД
    """Adding a comment to market"""
    db_curs.execute("""INSERT INTO Comments VALUES (?,?)""", (comment, id_market))
    db_conn.commit()


def rating(db_curs, db_conn, rating_m, id_market):   # Добавление рейтинга в БД
    """Adding a rating to market"""
    db_curs.execute("""INSERT INTO Ratings VALUES (?,?)""", (rating_m, id_market))
    db_conn.commit()


def distance(la1, lo1, la2, lo2):           # расчет дистанции между 2 координатами
    """determining the distance by coordinates"""
    lo1 = radians(lo1)
    lo2 = radians(lo2)
    la1 = radians(la1)
    la2 = radians(la2)

    d_lo = lo2 - lo1
    d_la = la2 - la1
    d_p = sin(d_la / 2) ** 2 + cos(la1) * cos(la2) * sin(d_lo / 2) ** 2
    result = ((2 * asin(sqrt(d_p))) * 3959)
    return result


def dist_btwn_m(db_curs, market1, market2):     # расчет дистанции между рынками
    """determining the distance between markets"""
    db_curs.execute("""SELECT LocX, LocY FROM Addresses WHERE
    idMarket = ?""", (market1, ))
    mrkt1 = db_curs.fetchone()
    db_curs.execute("""SELECT LocX, LocY FROM Addresses WHERE
    idMarket = ?""", (market2, ))
    mrkt2 = db_curs.fetchone()

    lo1 = radians(float(mrkt1[0]))
    lo2 = radians(float(mrkt2[0]))
    la1 = radians(float(mrkt1[1]))
    la2 = radians(float(mrkt2[1]))

    d_lo = lo2 - lo1
    d_la = la2 - la1
    d_p = sin(d_la / 2) ** 2 + cos(la1) * cos(la2) * sin(d_lo / 2) ** 2
    result = ((2 * asin(sqrt(d_p))) * 3959)
    return result


def comm_market(db_curs, idmarket):         # коммнтарии магазина
    """add comments about the market"""
    cmnts = []
    db_curs.execute("""SELECT Comment FROM Comments WHERE idMarket = ?""", (idmarket, ))
    for i in db_curs:
        cmnts.append(i)
    return cmnts


def rating_market(db_curs, idmarket):         # средний рейтинг магазина
    """add rating about the market"""
    ratings = []
    db_curs.execute("""SELECT AVG(Rating) FROM Ratings WHERE idMarket = ?""", (idmarket, ))
    for i in db_curs:
        ratings.append(i)
    return ratings
# endregion


if __name__ == '__main__':
    try:
        file_db = input("specify DB name and dir ==> ")
        conn, curs = init(file_db)
        file_name = input("specify CSV filename and dir ==> ")
        etl(conn, curs, file_name)
        insert_city(conn, curs)
        insert_county(conn, curs)
        insert_state(conn, curs)
        close(conn, curs)
        print("THE DataBase is ready")
    except PermissionError:
        print("Something went wrong, check CSV file")
    except FileNotFoundError:
        print("Something went wrong, check CSV file")
    except sqlite3.IntegrityError:
        print("Problems with Data Base. Maybe Data Base is already exist")

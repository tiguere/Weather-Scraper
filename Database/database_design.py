"""
scraping project - part 2
database generation module
"""

import mysql.connector

DB_name = 'weather'
tables = {
    'Locations':
        (
            "CREATE TABLE IF NOT EXISTS `Locations` ("
            "  `Id` int NOT NULL AUTO_INCREMENT,"
            "  `Name` varchar(255) NOT NULL,"
            "  `BBC_Id` varchar(10) NOT NULL,"
            "  PRIMARY KEY (`Id`), UNIQUE KEY `name` (`name`)"
            ") ENGINE=InnoDB"
        ),
    'Forecasts':
        (
            "CREATE TABLE IF NOT EXISTS `Forecasts` ("
            "  `Id` int NOT NULL AUTO_INCREMENT,"
            "  `Scrape_Date` date NOT NULL,"
            "  `Location` text NOT NULL,"
            "  `Date` date NOT NULL,"
            "  `Hour` int  NOT NULL,"
            "  `Temperature_C` int NOT NULL,"
            "  `Chance_of_Rain` int NOT NULL,"
            "  `Wind_Speed_Kph` int NOT NULL,"
            "  `Percent_Humidity` int NOT NULL,"
            "  `Pressure_Mb` int NOT NULL,"
            "  `Feels_Like_C` int NOT NULL,"
            "  `Location_Id` int NOT NULL,"
            "  FOREIGN KEY (`Location_Id`)  REFERENCES `Locations` (`Id`),"
            "  PRIMARY KEY (`Id`)"
            ") ENGINE=InnoDB"
        ),
    'Historical':
        (
            "CREATE TABLE IF NOT EXISTS `Historical` ("
            "  `Id` int NOT NULL AUTO_INCREMENT,"
            "  `Scrape_Date` date NOT NULL,"
            "  `Location` text NOT NULL,"
            "  `Date` date NOT NULL,"
            "  `Hour` int  NOT NULL,"
            "  `Temperature_C` int NOT NULL,"
            "  `Weather` varchar(30) NOT NULL,"
            "  `Wind_Speed_Kph` int NOT NULL,"
            "  `Percent_Humidity` int NOT NULL,"
            "  `Pressure_Mb` int NOT NULL,"
            "  `Visibility_Km` int NOT NULL,"
            "  `Location_Id` int NOT NULL,"
            "  FOREIGN KEY (`Location_Id`) REFERENCES `Locations` (`Id`),"
            "  PRIMARY KEY (`Id`)"
            ") ENGINE=InnoDB"
        )}


def connection():

    try:
        con = mysql.connector.connect(host='localhost', database='mysql', user='root')
    except Exception as e:
        print(f"failed to connect:{e}")
        exit(1)
    else:
        return con


def create_database(cursor, DB_name):

    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_name}")
    except mysql.connector.Error as err:
        print(f'failed creating database:{err}')
        exit(1)
    else:
        print(f"CREATE DATABASE:{DB_name}")


def create_tables(cursor, table_dict):

    for table_name in tables:
        try:
            cursor.execute(table_dict[table_name])
        except mysql.connector.Error as err:
            print(f"failed to create a table:{table_name}, {err}")
            exit(1)
        else:
            print(f"table:{table_name}, created")


def main():

    con = connection()
    cursor = con.cursor()
    create_database(cursor, DB_name=DB_name)
    try:
        cursor.execute(f"USE {DB_name}")
    except mysql.connector.Error as err:
        print(f"failed to use Database: {DB_name}.")
        exit(1)

    create_tables(cursor, tables)
    cursor.close()
    con.close()


if __name__ == '__main__':

    main()




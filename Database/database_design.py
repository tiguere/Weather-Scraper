"""
scraping project - part 2
database generation module
"""

import mysql.connector
import config as cfg

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
        ),
    'Pollution':
        (
            "CREATE TABLE IF NOT EXISTS `Pollution` ("
            "  `Location_Id` int NOT NULL,"
            "  `location` varchar(30),"
            "  `date` date,"
            "  `time` int,"
            "  `CO` float,"
            "  `NO` float,"
            "  `NO2` float,"
            "  `O3` float,"
            "  `SO2` float,"
            "  `NH3` float,"
            "  `PM2_5` float,"
            "  `PM10` float,"
            "  FOREIGN KEY (`Location_Id`) REFERENCES `Locations` (`Id`)"
            ") ENGINE=InnoDB"
        )
}


def connection():
    try:
        con = mysql.connector.connect(host='localhost', database='mysql', user=cfg.DB_USER, password=cfg.DB_PASS)
    except Exception as e:
        print(f"failed to connect:{e}")
        exit(1)
    else:
        return con


def create_database(cursor, DB_name):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_name}")
        print(f"SUCCESSFULLY CREATED DATABASE: {DB_name} ")
    except mysql.connector.Error as err:
        print(f'FAILED TO CREATE DATABASE:{err}')
        exit(1)
    else:
        print(f"DATABASE ALREADY EXISTS: {DB_name} ")


def create_tables(cursor, table_dict):
    for table_name in table_dict.keys():
        try:
            cursor.execute(table_dict[table_name])
        except mysql.connector.Error as err:
            print(f"FAILED TO CREATE TABLE:{table_name}, {err}")
            exit(1)
        else:
            print(f"TABLE ALREADY EXISTS: {table_name}")


def main():
    con = connection()
    cursor = con.cursor()
    create_database(cursor, DB_name=DB_name)
    try:
        cursor.execute(f"USE {DB_name}")
    except mysql.connector.Error as err:
        print(f"FAILED TO CONNECT TO: {DB_name}.")
        exit(1)

    create_tables(cursor, tables)
    cursor.execute('ALTER DATABASE weather CHARACTER SET utf8 COLLATE utf8_general_ci;')
    cursor.execute('ALTER TABLE Locations CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;')
    cursor.close()
    con.close()


if __name__ == '__main__':
    main()




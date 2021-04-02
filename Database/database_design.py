import mysql.connector


DB_name = 'weather'
tables = {}

tables['location'] = (
    "CREATE TABLE IF NOT EXISTS `location` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(50) NOT NULL,"
    "  PRIMARY KEY (`id`), UNIQUE KEY `name` (`name`)"
    ") ENGINE=InnoDB")

tables['Forecasts'] = (
    "CREATE TABLE IF NOT EXISTS `Forecasts` ("
    "  `date` date NOT NULL,"
    "  `Hour` int  NOT NULL,"
    "  `Temperature_C` int NOT NULL,"
    "  `Percent_Chance_of_Rain` int NOT NULL,"
    "  `Wind_Speed_mph` int NOT NULL,"
    "  `Percent_Humidity` int NOT NULL,"
    "  `Pressure_ mb` int NOT NULL,"
    "  `Feels_Like_C` int NOT NULL,"
    "  `location_id` int NOT NULL,"
    "  FOREIGN KEY (`location_id`)"
    "  REFERENCES `location` (`id`)"
    ") ENGINE=InnoDB")

tables['Actual'] = (
    "CREATE TABLE IF NOT EXISTS `Actual` ("
    "  `date` date NOT NULL,"
    "  `Time` int  NOT NULL,"
    "  `Temp_C` int NOT NULL,"
    "  `Weather` varchar(30) NOT NULL,"
    "  `Wind_km/h` int NOT NULL,"
    "  `Percent_Humidity` int NOT NULL,"
    "  `Pressure_ mb` int NOT NULL,"
    "  `Visibility_km` int NOT NULL,"
    "  `location_id` int NOT NULL,"
    "  FOREIGN KEY (`location_id`)"
    "  REFERENCES `location` (`id`)"
    ") ENGINE=InnoDB")


def connection():

    try:
        con = mysql.connector.connect(host='localhost',database='mysql',user='root')
    except Exception as e:
        print(f"failed to connect:{e}")
        exit(1)
    else:
        print("connected")
        return con



def create_database(cursor,DB_name):

    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_name}")
    except mysql.connector.Error as err:
        print(f'failed creating database:{err}')
        exit(1)
    else:
        print(f"CREATE DATABASE:{DB_name}")


def create_tables(cursor,tables):

    for table_name in tables:
        try:
            cursor.execute(tables[table_name])
        except mysql.connector.Error as err:
            print(f"failed to create a table:{table_name},{err}")
            exit(1)
        else:
            print(f"table:{table_name}, created")


def main():

    con = connection()
    cursor = con.cursor()
    create_database(cursor,DB_name=DB_name)
    try:
        cursor.execute(f"USE {DB_name}")
    except mysql.connector.Error as err:
        print(f"failed to use Database: {DB_name}.")
        exit(1)

    create_tables(cursor,tables)


if __name__ == '__main__':

    main()




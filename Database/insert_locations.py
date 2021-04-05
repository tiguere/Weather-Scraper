"""
scraping project - part 2
insert locations module
"""

import mysql.connector


def insert_location(cur, city, city_id):
    cur.execute(f'''SELECT * FROM weather.Locations WHERE Name = '{city}' 
                OR BBC_Id = '{city_id}'
                ''')
    all_rows = cur.fetchall()
    row_count = len(all_rows)
    print(f"Total rows in Locations table for given location {city} are: {row_count}")
    if row_count == 0:
        print("trying insert...")
        try:
            cur.execute(f'''INSERT INTO weather.Locations (
                                              Name,
                                              BBC_Id
                                              ) VALUES (
                                                '{city}', 
                                                '{city_id}')''')
        except mysql.connector.Error as err:
            print(f"{err}: failed to insert for : \n{city} and {city_id}.")
            exit(1)
    else:
        print(f"skipping Insert to Locations because this city {city} already in database")
        pass

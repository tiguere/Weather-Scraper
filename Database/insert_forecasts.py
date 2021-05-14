"""
scraping project - part 2
insert forecasts module
"""

import mysql.connector


def insert_forecasts(cur, row, city_id):
    cur.execute(f'''SELECT * FROM weather.Forecasts WHERE Date = '{row.Date}' 
            AND Hour = '{row.Hour}' 
            AND Date = '{row.Date}'
            AND Temperature_C = '{row.Temperature_C}'
            AND Chance_of_Rain = '{row.Chance_of_Rain}'
            AND Wind_Speed_Kph = '{row.Wind_Speed}'
            AND Percent_Humidity = '{row.Humidity}'
            AND Pressure_Mb = '{row.Pressure}'
            AND Feels_Like_C = '{row.Feels_Like_C}'
            AND Location_Id = '{city_id}'
            ''')
    all_rows = cur.fetchall()
    row_count = len(all_rows)
    if row_count == 0:
        try:
            cur.execute(f'''INSERT INTO weather.Forecasts (
                                          Scrape_Date,
                                          Date,
                                          Hour,
                                          Temperature_C,
                                          Chance_of_Rain,
                                          Wind_Speed_Kph,
                                          Percent_Humidity,
                                          Pressure_Mb,
                                          Feels_Like_C,
                                          Location_Id
                                          ) VALUES (
                                            '{row.Scrape_Date}',
                                            '{row.Date}',
                                            '{row.Hour}',
                                            '{row.Temperature_C}',
                                            '{row.Chance_of_Rain}',
                                            '{row.Wind_Speed}',
                                            '{row.Humidity}',
                                            '{row.Pressure}',
                                            '{row.Feels_Like_C}',
                                            '{city_id}')''')
            print(f"WEATHER FORECAST INSERTED FOR CITY OF ID: {city_id} on {row.Date} at {row.Hour}")
        except mysql.connector.Error as err:
            print(f"{err}: failed to insert for row: \n{row}.")
            exit(1)
    else:
        print(f"skipping Insert to Forecasts because this data already exists in database:\n{row} ")
        pass

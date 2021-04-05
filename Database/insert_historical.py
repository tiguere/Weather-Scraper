"""
scraping project - part 2
insert historical data module
"""

import mysql.connector


def insert_historical(cur, row, city_id):
    cur.execute(f'''SELECT * FROM weather.Historical WHERE Date = '{row.Date}' 
            AND Location = '{row.Location}' 
            AND Date = '{row.Date}'
            AND Hour = '{row.Time}'
            AND Temperature_C = '{row.Temp}'
            AND Weather = '{row.Weather}'
            AND Wind_Speed_Kph = '{row.Wind}'
            AND Percent_Humidity = '{row.Humidity}'
            AND Pressure_Mb = '{row.Pressure}'
            AND Visibility_Km = '{row.Visibility}'
            AND Location_Id = '{city_id}'
            ''')
    all_rows = cur.fetchall()
    row_count = len(all_rows)
    if row_count == 0:
        try:
            cur.execute(f'''INSERT INTO weather.Historical (
                                          Scrape_Date,
                                          Location,
                                          Date,
                                          Hour,
                                          Temperature_C,
                                          Weather,
                                          Wind_Speed_Kph,
                                          Percent_Humidity,
                                          Pressure_Mb,
                                          Visibility_Km,
                                          Location_Id
                                          ) VALUES (
                                            '{row.Scrape_Date}',
                                            '{row.Location}', 
                                            '{row.Date}',
                                            '{row.Time}',
                                            '{row.Temp}',
                                            '{row.Weather}',
                                            '{row.Wind}',
                                            '{row.Humidity}',
                                            '{row.Pressure}',
                                            '{row.Visibility}',
                                            '{city_id}')''')
            print(f"HISTORICAL WEATHER INSERTED FOR: {row.Location} on {row.Date} at {row.Time}")
        except mysql.connector.Error as err:
            print(f"{err}: failed to insert for row: \n{row}.")
            exit(1)
    else:
        print(f"skipping Insert to Historical because this data already exists in database:\n{row} ")
        pass


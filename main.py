"""
scraping project - part 2
scraping hourly forecasts from BBC.com/weather as well as
actual historical weather data from timeanddate.com
for major cities around the world and storing in database
"""


import pandas as pd
import os
import config as cfg
import click
import logging
from forecasts import get_forecasts_city_page
from forecasts import get_next_day
from forecasts import download_primary_data
from forecasts import download_secondary_data
from historicals import get_historical_weather
from Database.database_design import connection
from Database.insert_forecasts import insert_forecasts
from Database.get_location_id import get_location_id
from Database.insert_historical import insert_historical
from Database.insert_locations import insert_location


# CONFIGURATION OF LOGGER
logging.basicConfig(
    filename='Scrape Logs/scrape_log.log',
    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNCTION:%(funcName)s-LINE:%(lineno)d-%(message)s',
    level=logging.INFO)


def write_location(location, city_id):
    con = connection()
    cursor = con.cursor()
    insert_location(cursor, location, city_id)
    con.commit()
    cursor.close()
    con.close()


def write_forecasts(city_name, listed):
    """
    receives data, creates DataFrame and write it to csv file
    :param city_name: the city name
    :param listed: the list passed in
    """
    df = pd.DataFrame(listed, columns=["Scrape_Date",
                                       "Location",
                                       "Date",
                                       "Hour",
                                       "Temperature_C",
                                       "Chance_of_Rain",
                                       "Wind_Speed",
                                       "Humidity",
                                       "Pressure",
                                       "Feels_Like_C"])
    df = df.astype(str)
    df = df.apply(lambda x: x.str.replace(r'[^\d.]+',
                                          '',
                                          regex=True) if x.name != 'Location' and x.name != 'Date' and x.name != 'Scrape_Date' else x)
    df = df.apply(lambda x: x.str.strip())
    con = connection()
    select_cursor = con.cursor(buffered=True)
    insert_cursor = con.cursor()
    location_id = get_location_id(select_cursor, city_name)
    select_cursor.close()
    df.apply(lambda x: insert_forecasts(insert_cursor, x, location_id), axis=1)
    con.commit()
    insert_cursor.close()
    con.close()


def write_historical_weather(city_name, df):
    """
    receives data and inserts in mysql database
    :param city_name: the historical data dataframe of past weather
    :param df: the historical data dataframe of past weather
    """
    df = df.astype(str)
    df = df.apply(lambda x: x.str.replace(r'[^\d.]+', '', regex=True) if x.name != 'Location' and x.name != 'Date' and x.name != 'Scrape_Date' and x.name != 'Weather' else x)
    df = df.apply(lambda x: x.str.strip())
    df.replace("", "-1", inplace=True)
    con = connection()
    select_cursor = con.cursor(buffered=True)
    insert_cursor = con.cursor()
    location_id = get_location_id(select_cursor, city_name)
    select_cursor.close()
    df.apply(lambda x: insert_historical(insert_cursor, x, location_id), axis=1)
    con.commit()
    insert_cursor.close()
    con.close()


@click.command()
@click.option('--days', default=14, type=click.IntRange(0, 14), help='Number of Days')
@click.option('--filename', default=cfg.FILENAME)
@click.option('--search_type',
              type=click.Choice(['forecast', 'historical'], case_sensitive=False),
              multiple=True,
              default=('forecast', 'historical'))
def main(filename, days, search_type):
    """
    The main function read from the city_list.xlsx file
    and scrape from each city page(url) from: https://www.bbc.com/weather/
    primary and secondary data. uploads the data into DataFrame
    and wright it to file.
    """
    print(f"You have chosen to scrape {', '.join(search_type)} weather data spanning {days} days.")
    current_path = os.path.abspath(os.getcwd())
    file_path = os.path.join(current_path, cfg.FOLDER_NAME, filename)
    df = pd.read_excel(file_path)
    df["location"] = df["city_ascii"] + ", " + df["country"]
    cities = list(df["location"])
    for city in cities:
        if 'forecast' in search_type:
            link_and_id = get_forecasts_city_page(city, cfg.FORECAST_URL)
            if link_and_id:
                link = link_and_id[0]
                city_id = link_and_id[1]
                write_location(city, city_id)
                for day in range(days):
                    day_soup = get_next_day(link+"/day"+str(day))
                    primary = download_primary_data(city, day, day_soup)
                    secondary = download_secondary_data(day_soup)
                    zipped_data = [zipped[0] + zipped[1] for zipped in zip(primary, secondary)]
                    write_forecasts(city, zipped_data)

            else:
                print(f'UNSUCCESSFUL ATTEMPT TO RETRIEVE CITY ID FOR FORECAST: {city}')
                logging.info(f'UNSUCCESSFUL ATTEMPT TO RETRIEVE CITY ID FOR FORECAST')
                pass
        if 'historical' in search_type:
            try:
                historical_weather = get_historical_weather(city, cfg.HISTORICAL_URL, days)
                write_historical_weather(city, historical_weather)
            except OSError:
                logging.info(f'Cannot find {city}')
                print(f"Cannot request", {city})
                pass


if __name__ == '__main__':
    main()
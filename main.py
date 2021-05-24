"""
scraping project - part 2
scraping hourly forecasts from BBC.com/weather as well as
actual historical weather data from timeanddate.com
for major cities around the world and storing in database
"""

import click
import pandas as pd
import os
import config as cfg
import time
import logging
from selenium.webdriver.firefox.options import Options
from forecasts import get_forecasts_city_page
from forecasts import get_next_day
from forecasts import download_primary_data
from forecasts import download_secondary_data
from historicals import get_historical_weather
from request_api import get_city_pollution
from request_api import insert_pollution
from Database import database_design
from Database.database_design import connection
from Database.insert_forecasts import insert_forecasts
from Database.get_location_id import get_location_id
from Database.insert_historical import insert_historical
from Database.insert_locations import insert_location


def selenium_config():
    """
    sets the headless config of selenium
    """
    options = Options()
    options.add_argument('-headless')
    return options


def logger_config():
    """
    configures logs in Logs directory
    """
    logging.basicConfig(filename='Logs/scrape_log.log',
                        format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNCTION:%(funcName)s-LINE:%(lineno)d-%(message)s',
                        level=logging.INFO)
    logging.info(f"Logger configured {time.ctime()}")


def write_location(location, city_id):
    """
    receives data, creates DataFrame and write it to csv file
    :param location: the location name to write
    :param city_id: the city_id to write
    """
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
                                          regex=True) if x.name not in ['Location',
                                                                        'Date',
                                                                        'Scrape_Date'] else x)
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
    df = df.apply(lambda x: x.str.replace(r'[^\d.]+',
                                          '',
                                          regex=True) if x.name not in ['Location',
                                                                        'Date',
                                                                        'Scrape_Date',
                                                                        'Weather'] else x)
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


def parse_arguments(cities, days, search_type, options):
    """
    receives data and inserts in mysql database
    :param cities: the list of cities
    :param days: the number days to span
    :param search_type: the search_type: "historical" or "forecast"
    :param options: the selenium webdriver's config options
    """
    for city in cities:
        logging.info(f'ATTEMPTING TO RETRIEVE CITY {city}')
        if 'forecast' in search_type:
            link_and_id = get_forecasts_city_page(city, cfg.FORECAST_URL, options)
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
                print(f'UNSUCCESSFUL ATTEMPT TO RETRIEVE CITY ID: {city}')
                logging.info(f'UNSUCCESSFUL ATTEMPT TO RETRIEVE CITY ID {city}')
                pass
        if 'historical' in search_type:
            try:
                historical_weather = get_historical_weather(city, cfg.HISTORICAL_URL, days, options)
                write_historical_weather(city, historical_weather)
            except OSError:
                logging.info(f'UNSUCCESSFUL ATTEMPT TO RETRIEVE HISTORICAL WEATHRE FOR {city}')
                print(f"UNSUCCESSFUL ATTEMPT TO RETRIEVE HISTORICAL WEATHER FOR {city}")
                pass
        if 'pollution' in search_type:
            try:
                pollution_data = get_city_pollution(city.split(",")[0], city.split(",")[1],
                                                    cfg.API_TOKEN, cfg.API_ENDPOINT)
                insert_pollution(pollution_data, city.split(",")[0])
            except OSError:
                logging.info(f'UNSUCCESSFUL ATTEMPT TO RETRIEVE POLLUTION FOR {city}')
                print(f"UNSUCCESSFUL ATTEMPT TO RETRIEVE POLLUTION FOR {city}")
                pass


@click.command()
@click.option('--days', default=14, type=click.IntRange(0, 14), help='Number of Days')
@click.option('--filename', default=cfg.FILENAME)
@click.option('--search_type',
              type=click.Choice(['forecast', 'historical', 'pollution'], case_sensitive=False),
              multiple=True,
              default=('forecast', 'historical'))
def main(days, filename, search_type):
    """
    The main function reads from your cities file
    and scrapes according to your request:
    """
    logger_config()
    logging.info(f"configuration of logger called: {time.ctime()}")
    database_design.main()
    options = selenium_config()
    logging.info(f"configuration of selenium called: {time.ctime()}")
    logging.info(f"Starting scrape: {time.ctime()}")
    print(f"You have chosen to scrape {', '.join(search_type)} weather data spanning {days} days.")
    current_path = os.path.abspath(os.getcwd())
    file_path = os.path.join(current_path, cfg.FOLDER_NAME, filename)
    df = pd.read_excel(file_path)
    df["location"] = df["city"] + ", " + df["country"]
    cities = list(df["location"])
    parse_arguments(cities, days, search_type, options)


if __name__ == '__main__':
    main()

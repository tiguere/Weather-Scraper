"""
scraping project - part 2
scraping hourly historical data from timeanddate.com/weather
for major cities around the world
"""

# from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import datetime
import logging


def get_previous_day(browser, day_num, location):
    try:
        select = browser.find_element_by_xpath('//*[@id="wt-his-select"]')
        select.click()
        day_num_option = browser.find_element_by_xpath('//*[@id="wt-his-select"]/option[' + str(day_num + 2) + ']')
        day_num_option.click()
        logging.info(f'SUCCESSFULY FOUND AND CLICKED DROPDOWN FOR {location}, day number {day_num}')
    except NoSuchElementException:
        logging.info(f'UNSUCCESSFUL CLICK FOR {location}: MOVING ON..')
        pass


def get_table(day_num, location, html):
    try:
        dfs = pd.read_html(html, header=0, skiprows=(0, 24))
        # Get second table
        df = dfs[1]
        today = datetime.date.today()
        df.loc[:, "Scrape_Date"] = today
        df.loc[:, "Date"] = today + datetime.timedelta(days=-day_num)
        df.loc[:, "Location"] = location
        df = df.iloc[:-1, :]
        df = df[["Scrape_Date",
                 "Location",
                 "Date",
                 "Time",
                 "Temp",
                 "Weather",
                 "Wind",
                 "Humidity",
                 "Barometer",
                 "Visibility"]]
        df.rename(columns={"Barometer":"Pressure"},inplace=True)
        df["Pressure"] = df["Pressure"].str.rstrip("ar")
        return df
    except ValueError:
        logging.info(f' NO TABLES FOR: {location} MOVING ON..')
        pass


def get_historical_weather(location, url, num_days, options):
    """
    receives city-name+location and send it as key to the browser (URL),
    receives back the page of the city and returns the current url
    :param location: location passed in as (city, country)
    :param url: url of historical weather web page
    :param num_days: number of days to look back
    :param options: the selenium config options
    :return city_page: the path to the city weather page(s)
    """
    city_name = location.split(", ")[0].replace(" ", "-")
    country_name = location.split(", ")[1].replace(" ", "-")
    city_url = url+country_name+"/"+city_name+"/historic"
    browser = webdriver.Firefox(options=options)
    time.sleep(1)
    try:
        browser.get(city_url)
    except OSError:
        logging.info(f' UNSUCCESSFUL GET REQUEST FOR: {location} MOVING ON..')
    historical_data = pd.DataFrame()
    for day in range(1, num_days+1):
        get_previous_day(browser, day, location)
        time.sleep(1)
        page_text = browser.page_source
        data = get_table(day, location, page_text)
        historical_data = historical_data.append(data)
    browser.close()
    browser.quit()
    return historical_data

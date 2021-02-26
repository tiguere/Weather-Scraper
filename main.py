"""
scraping project - part 1
scraping hourly forecasts from BBC.com/weather
for major cities around the world
"""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument('-headless')
import pandas as pd
from bs4 import BeautifulSoup
import logging
import requests
import re
import time
import datetime
import os
import config as CFG


# CONFIGURATION OF LOGGER
logging.basicConfig(
    filename='weather_scrape.log',
    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNCTION:%(funcName)s-LINE:%(lineno)d-%(message)s',
    level=logging.INFO)


def get_city_page(city, url):
    """
    receives city-name+location and send it as key to the browser (URL),
    receives back the page of the city and returns the current url
    :param city: name of city passed in
    :param url: url of main bbc weather web page
    :return city_page: the path to the city weather page(s)
    """
    browser = webdriver.Firefox(options=options)
    time.sleep(1)
    browser.get(url)
    search = browser.find_element_by_xpath('//*[@id="ls-c-search__input-label"]')
    search.send_keys(city)
    time.sleep(1)
    try:
        time.sleep(1)
        first_result = browser.find_element_by_xpath('//*[@id="location-list"]/li[2]/a')
        first_result.click()
    except:
        logging.info(f'UNSUCCESSFUL CLICK: MOVING ON..')
        city_page = False
    else:
        logging.info(f'SUCCESSFULY FOUND {city} IN DROPDOWN')
        city_page = browser.current_url
    return city_page


def get_next_day(link):
    """
    :param link: city weather day-specific link passed in
    :return soup: a BeautifulSoup object for the specific link (specific day)
    """

    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def download_primary_data(city, day_num, soup):
    """
    :param city: city name passed in
    :param day_num: the number of days to offset from today
    :param soup: the soup object to parse
    :return a list of primary hourly forecast data scraped from the city page in the specific day
    """

    today = datetime.date.today()
    hours_at_day = soup.find_all(class_="wr-time-slot-primary wr-js-time-slot-primary")
    date = today + datetime.timedelta(days=day_num)
    data = []
    for hour in hours_at_day:
        time_of_day = hour.find('span', class_="wr-time-slot-primary__hours wr-u-font-weight-500").text
        if 0 <= int(time_of_day) <= 5:
            date = today + datetime.timedelta(days=day_num+1)
        date_string = date.strftime('%Y-%m-%d')
        temperature = hour.find('span', class_="wr-value--temperature--c").text
        chance_of_precipitation = re.sub(r"[a-z]", '', hour.find('div', class_="wr-u-font-weight-500").text)
        wind_speed = hour.find('span', class_="wr-value--windspeed wr-value--windspeed--mph").text
        data.append([city, date_string, time_of_day, temperature, chance_of_precipitation, wind_speed])
    return data


def download_secondary_data(soup):
    """
    :param soup: soup object passed in
    :return data: a list of secondary hourly forecast data scraped from the city page in the specific day
    """
    data = []
    secondary_list = soup.find_all("dl", class_="wr-time-slot-secondary__list")
    for hour in secondary_list:
        data_by_hour = hour.find_all('dd')
        humidity = data_by_hour[0].text
        pressure = data_by_hour[1].text
        temperature_c, temperature_f = re.split(r'\D+', secondary_list[0].parent.next_sibling.text.split()[3])[:2]
        data.append([humidity, pressure, temperature_c])
    return data


def write_to_file(count, listed):
    """
    receives data, creates DataFrame and write it to csv file
    :param count: the count of cities
    :param listed: the list passed in
    """

    df = pd.DataFrame(listed)
    if count > 0:
        df.to_csv('test.csv', mode='a', header=False)
    else:
        df.to_csv('test.csv', mode='a', header=["City",
                                                "Date",
                                                "Hour",
                                                "Temperature (C)",
                                                "Chance of Rain",
                                                "Wind Speed",
                                                "Humidity",
                                                "Pressure",
                                                "Feels Like (C)"])


def main():
    """The main function read from the city_list.xlsx file
           and scrape from each city page(url) from: https://www.bbc.com/weather/
           primary and secondary data. uploads the data into DataFrame
           and wright it to file.
        """

    current_path = os.path.abspath(os.getcwd())
    file_path = os.path.join(current_path, CFG.FOLDER_NAME, CFG.FILENAME)
    df = pd.read_excel(file_path)
    df["location"] = df["city"] + ", " + df["country"]
    cities = list(df["location"])
    city_count = 0
    for city in cities:
        link = get_city_page(city, CFG.URL)
        if link:
            for day in range(0, 14):
                day_soup = get_next_day(link+"/day"+str(day))
                primary = download_primary_data(city, day, day_soup)
                secondary = download_secondary_data(day_soup)
                zipped_data = [zipped[0] + zipped[1] for zipped in zip(primary, secondary)]
                write_to_file(city_count, zipped_data)
        else:
            pass
        city_count += 1


if __name__ == '__main__':
    main()
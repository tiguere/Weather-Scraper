from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument('-headless')
import pandas as pd
from bs4 import BeautifulSoup
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import requests
import re
import time
import datetime
import os
import config as CFG


## CONFIGURATION OF LOGGER
logging.basicConfig(
    filename='movies.log',
    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNCTION:%(funcName)s-LINE:%(lineno)d-%(message)s',
    level=logging.INFO)


def get_city_page(city, url):
    browser = webdriver.Firefox()#options=options
    time.sleep(1)
    browser.get(url)
    search = browser.find_element_by_xpath('//*[@id="ls-c-search__input-label"]')
    search.send_keys(city)
    time.sleep(2)
    try:
        first_result = browser.find_element_by_xpath('//*[@id="location-list"]/li[2]/a')
        first_result.click()
    except RuntimeError:
        logging.info(f'UNSUCCESSFUL CLICK: MOVING ON..')
        city_page = False
        pass
    else:
        logging.info(f'SUCCESSFULY FOUND {city} IN DROPDOWN')
    city_page = browser.current_url
    return city_page


def get_next_day(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def download_primary_data(city, day_num, soup):
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
    # create loop that looks for each element that contain the "hourly" forecast in the soup
    # account for the fact that there is overlap between days in the carousel
    # for e in elements (the hourly elements):
        # list_of_data = []
        # looking through "secondary" elements
        # append to list_of_data
    # call write_to_file(list)
    # return list_of_secondary_data
    data = []
    secondary_list = soup.find_all("dl", class_="wr-time-slot-secondary__list")
    for hour in secondary_list:
        data_by_hour = hour.find_all('dd')
        humidity = data_by_hour[0].text
        pressure = data_by_hour[1].text
        temperature_c, temperature_f = re.split(r'\D+', secondary_list[0].parent.next_sibling.text.split()[3])[:2]
        data.append([humidity, pressure, temperature_c])
    return data


def write_to_file():
    pass


def main():
    current_path = os.path.abspath(os.getcwd())
    file_path = os.path.join(current_path, CFG.FOLDER_NAME, CFG.FILENAME)
    df = pd.read_excel(file_path)
    df["location"] = df["city"] + ", " + df["country"]
    cities = list(df["location"])
    for city in cities:
        link = get_city_page(city, CFG.URL)
        if link:
            for day in range(0, 14):
                day_soup = get_next_day(link+"/day"+str(day))
                primary = download_primary_data(city, day, day_soup)
                secondary = download_secondary_data(day_soup)
                zipped = list(zip(primary, secondary))
                df = pd.DataFrame(zipped)
                if day == 0:
                    df.to_csv('test.csv', mode='a', header=True)
                else:
                    df.to_csv('test.csv', mode='a', header=False)
            break

        # download_secondary_data
        # write_to_file
    pass


if __name__ == '__main__':
    main()
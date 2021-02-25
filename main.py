from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument('-headless')
import pandas as pd
from bs4 import BeautifulSoup
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

URL = "https://www.bbc.com/weather/"
FILENAME = "city_list.xlsx"
FOLDER_NAME = "Cities"


def get_city_page(city, url):
    browser = webdriver.Firefox()#options=options
    time.sleep(1)
    browser.get(url)
    search = browser.find_element_by_xpath('//*[@id="ls-c-search__input-label"]')
    search.send_keys(city)
    time.sleep(2)
    first_result = browser.find_element_by_xpath('//*[@id="location-list"]/li[2]/a')
    first_result.click()
    city_page = browser.current_url
    return city_page


def get_next_day(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def download_primary_data(day_num, soup):
    today = datetime.date.today()
    date = today + datetime.timedelta(days=day_num)
    date_string = date.strftime('%Y-%m-%d')
    hours = soup.findAll('span',{'class':'wr-time-slot-primary__hours'})
    temperatures = soup.findAll('span', {'class': 'wr-value--temperature--c'})
    chance_of_precipitations = soup.findAll('div', {'class': 'wr-time-slot-primary__precipitation'})
    wind_speeds = soup.findAll('span', {'class': 'wr-value--windspeed'})
    print(wind_speeds)
    for (hour, temp, chance, wind) in zip(hours, temperatures, chance_of_precipitations, wind_speeds):
        chance_value = chance.find('div', {'class': "wr-u-font-weight-500"})
        hour_record = [date_string]
        hour_record.extend([hour.text, temp.text, chance_value.text, wind.text])
    return hour_record


def download_secondary_data(soup):
    # create loop that looks for each element that contain the "hourly" forecast in the soup
    # account for the fact that there is overlap between days in the carousel
    # for e in elements (the hourly elements):
        # list_of_data = []
        # looking through "secondary" elements
        # append to list_of_data
    # call write_to_file(list)
    # return list_of_secondary_data
    pass

def write_to_file():
    pass


def main():
    current_path = os.path.abspath(os.getcwd())
    file_path = os.path.join(current_path, FOLDER_NAME, FILENAME)
    df = pd.read_excel(file_path)
    df["location"] = df["city"] + ", " + df["country"]
    cities = list(df["location"])
    for city in cities:
        link = get_city_page(city, URL)
        print(link)
        for day in range(0, 14):
            day_soup = get_next_day(link+"/day"+str(day))
            download_primary_data(day, day_soup) #primary =
        break
        # download_secondary_data
        # write_to_file
    pass


if __name__ == '__main__':
    main()
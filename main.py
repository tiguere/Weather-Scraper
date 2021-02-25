from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import requests
import time
import os

URL = "https://www.bbc.com/weather/"


def get_city_page(city, url):
    browser = webdriver.Firefox()
    time.sleep(1)
    browser.get(url)
    search = browser.find_element_by_xpath('//*[@id="ls-c-search__input-label"]')
    search.send_keys(city)
    time.sleep(1)
    first_result = browser.find_element_by_xpath('//*[@id="location-list"]/li[2]/a')
    first_result.click()
    city_page = browser.current_url
    return city_page


def get_next_day():
    # in a loop, get https://www.bbc.com/weather/293397/DayX (where x is a number from 1 to 14)
    # create beautiful soup on each path
    # parse and return object
    # e.g. "soup"
    day = requests.get(os.path.join(url, "day{}".format(day_number)))
    soup = BeautifulSoup(day.content, 'html.parser')
    return soup


def download_primary_data(soup):
    # create loop that looks for each element that contain the "hourly" forecast in the soup
    # account for the fact that there is overlap between days in the carousel
    # for e in elements (the hourly elements):
        # list_of_data = []
        # looking through "primary" elements
        # append to list_of_data
    # return nested list_of_primary_data by each hour at day
    data = []
    hours_at_day = soup.find_all(class_="wr-time-slot-primary wr-js-time-slot-primary")
    for hour in hours_at_day:
        Time = hour.find('span', class_="wr-time-slot-primary__hours wr-u-font-weight-500").text
        Temperature = hour.find('span', class_="wr-value--temperature--c").text
        chance_of_precipitation = re.sub(r"[a-z]", '', hour.find('div', class_="wr-u-font-weight-500").text)
        windspeed = hour.find('span', class_="wr-value--windspeed wr-value--windspeed--mph").text
        data.append([Time, Temperature, chance_of_precipitation, windspeed])
    return data


def download_secondary_data(soup):
    # create loop that looks for each element that contain the "hourly" forecast in the soup
    # account for the fact that there is overlap between days in the carousel
    # for e in elements (the hourly elements):
        # list_of_data = []
        # looking through "secondary" elements
        # append to list_of_data
    # call write_to_file(list)
    # return nested list_of_secondary_data by each hour at day
    data = []
    secondary_list = soup.find_all("dl", class_="wr-time-slot-secondary__list")
    for hour in secondary_list:
        data_by_hour = hour.find_all('dd')
        Humidity = data_by_hour[0].text
        Pressure = data_by_hour[1].text
        Temperature_C, Temperature_F = re.split(r'\D+', secondary_list[0].parent.next_sibling.text.split()[3])[:2]
        data.append([Humidity, Pressure, Temperature_C, Temperature_F])
    return data


def write_to_file():
    pass


def main():
    # LOOP:
    get_city_page("Amsterdam, Netherlands", URL)
    # LOOP (TO 14):
        # get_next_day
        # download_primary_data
        # download_secondary_data
        # write_to_file
    pass


if __name__ == '__main__':
    main()
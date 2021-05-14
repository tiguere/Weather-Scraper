"""
scraping project - part 2
scraping hourly forecasts from BBC.com/weather
for major cities around the world
"""

# from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import requests
import re
import time
import datetime
import logging


def get_forecasts_city_page(city, url, options):
    """
    receives city-name+location and send it as key to the browser (URL),
    receives back the page of the city and returns the current url
    :param city: name of city passed in
    :param url: url of main bbc weather web page
    :param options: the selenium config options
    :return city_page: the path to the city weather page(s)
    """
    browser = webdriver.Firefox(options=options)
    browser.get(url)
    time.sleep(1)
    try:
        search = browser.find_element_by_xpath('//*[@id="ls-c-search__input-label"]')
        search.send_keys(city)
    except NoSuchElementException:
        logging.info(f'UNSUCCESSFUL SEARCH FOR CITY VALUE INPUT FOR {city}: MOVING ON..')
        pass
    time.sleep(1)
    try:
        selector = '#location-list.ls-c-locations-list-list li.ls-c-locations-list-item'
        results = browser.find_elements_by_css_selector(selector)
        if results:
            first_result = results[0]
            first_result.click()
        else:
            logging.info(f'NO LOCATION LIST FOR FOR {city}: MOVING ON..')
    except NoSuchElementException:
        logging.info(f'UNSUCCESSFUL CLICK FOR {city}: MOVING ON..')
        print(f"Couldn't click on result for {city}")
        city_page = False
        return city_page
    else:
        logging.info(f'SUCCESSFULLY FOUND {city} IN DROPDOWN')
        city_page = browser.current_url
        city_id = browser.current_url.split("/")[-1]
        return city_page, city_id
    browser.close()
    browser.quit()


def get_next_day(link):
    """
    receives link to weather webpage for specific day in future for city, e.g. BBC.com/weather/<CITY ID>/<DAY NUMBER>
    returns that page's soup object
    :param link: city weather day-specific link passed in
    :return soup: a BeautifulSoup object for the specific link (specific day)
    """
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def download_primary_data(city, day_num, soup):
    """
    receives soup object along with city name and relevant day number for storage purposes
    returns that city's primary weather data for that day in the future
    e.g. hour of day, temperature value, precipitation, wind speed
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
        wind_speed = hour.find('span', class_="wr-value--windspeed wr-value--windspeed--kph").text.split(" ")[0]
        data.append([today, city, date_string, time_of_day, temperature, chance_of_precipitation, wind_speed])
    return data


def download_secondary_data(soup):
    """
    receives soup object of specific city weather data for day in future
    returns that city's primary weather data for that day in the future
    e.g. hour of day, temperature value, precipitation, wind speed
    :param soup: soup object passed in
    :return data: a list of secondary hourly forecast data scraped from the city page in the specific day
    """
    data = []
    secondary_list = soup.find_all("dl", class_="wr-time-slot-secondary__list")
    for hour in secondary_list:
        data_by_hour = hour.find_all('dd')
        humidity = data_by_hour[0].text
        pressure = data_by_hour[1].text.split(" ")[0]
        temperature_c, temperature_f = re.split(r'\D+', secondary_list[0].parent.next_sibling.text.split()[3])[:2]
        data.append([humidity, pressure, temperature_c])
    return data

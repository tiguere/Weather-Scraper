ITC-Scrape -  Weather Scraper
===

A scraping utility which downloads, past(historicals) or/and future(forecasts), high-resolution weather data,
around the world.

The historicals data are scraping from "www.timeanddate.com/weather" and allowing to scrape two weeks back of hourly data.

The future(forecasts) data, scraping from BBC's public weather stations around the world,
and allowing to scrape two weeks ahead of hourly data as well.
 
Using command line interface of click package, it can allow to choose the number of days which data is scraped (--days),
between 1 to 14 days range, backward(historicals) or/and forward(forecasts) (--search_type). 
Another option of the CLI, It allows to choose the list of locations for scrape the data (--filename).

By default, the list of cities are read from "city_list.xlsx".

All collected daily weather data(historicals,forecasts) outputs are set into Dataframe in the first step,
and then insert into the Database weather to the particular table according to the data source.

### The Database weather ###

The Database include three different tables of Locations, Forecasts and Historical data.

__Locations columns:__

Id: int NOT NULL AUTO_INCREMENT, PRIMARY KEY

Name: varchar(255), Location name

BBC_Id: varchar(10) NOT NULL, Location number in the url

__Forecasts columns:__

Id: int, NOT NULL, AUTO_INCREMENT, PRIMARY KEY

Scrape_Date: date, Date of the scrape

Location: text, Location name

Date: date, The day which the data scraped

Hour: int, The hour in the specific day

Temperature_C: int, Temperature in celsius

Chance_of_Rain: int, Chance percent of precipitation

Wind_Speed_Kph: int, Wind speed in kilometer per hour

Percent_Humidity: int, Percent of humidity

Pressure_Mb: int, Air pressure in millibar

Feels_Like_C: int, The feels like temperature in celsius

Location_Id: int, FOREIGN KEY, REFERENCES (Locations.Id)

__Historical columns:__

Id: int, NOT NULL, AUTO_INCREMENT, PRIMARY KEY

Scrape_Date: date, Date of the scrape

Location: text, Location name

Date: date, The day which the data scraped

Hour: int, The hour in the specific day

Temperature_C: int, Temperature in celsius

Weather: varchar(30), General description of tha day conditions

Wind_Speed_Kph: int, Wind speed in kilometer per hour

Percent_Humidity: int, Percent of humidity

Pressure_Mb: int, Air pressure in millibar

Visibility_Km: int, Visibility conditions in kilometer.

Location_Id: int, FOREIGN KEY, REFERENCES (Locations.Id)

 __ERD Diagram__ : 
 
 ![alt text](https://github.com/tiguere/ITC-Scrape/blob/master/Database/ERD_diagram.png?raw=true)
### Requirements ###

Python 3 or higher

Selenium Web Driver -- Please see https://www.selenium.dev/downloads/

Pandas

Requests

Beautiful Soup

MySQL Connector


```python
git clone https://github.com/tiguere/ITC-Scrape.git  
virtualenv ITC-Scrape  
source ITC-Scrape/bin/activate  
cd ITC-Scrape   
pip install -r requirements.txt
```


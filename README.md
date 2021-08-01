Weather Scraper
===

A scraping utility which retrieves historical and/or forecast weather data in high resolution, 
from major cities around the world.

Historical weather data is retrieved from <a href="www.timeanddate.com/weather">Time and Date</a> and enables collection of two weeks 
worth of hourly weather data.

Forecast weather data is retrieved from <a href="https://www.bbc.com/weather/293397">BBC weather<a/>,
enabling collection of up to two weeks worth of hourly data as well.

## Requirements

> * Python 3 or higher
> * <a href="https://www.selenium.dev/downloads/">Selenium Web Driver</a> **
> * Pandas
> * Requests
> * Beautiful Soup
> * MySQL Connector

****NOTE**
> This scraping utility uses a headless configuration of Firefox via Selenium, which
> requires a compatible webdriver to interface with the chosen browser, Firefox. 
> <a href="https://github.com/mozilla/geckodriver/releases">Mozilla Geckodriver</a> needs to be installed before the below examples can be run. 
> Make sure it’s in your PATH, e.g., place it in /usr/bin or /usr/local/bin.
> <br><br>
> **Failure to observe this step will give you the error: <br>```Selenium.common.exceptions.WebDriverException: Message: ‘geckodriver’ executable needs to be in PATH```.**

##  Usage ##

#### Installation
```
git clone https://github.com/tiguere/ITC-Scrape.git  
virtualenv ITC-Scrape  
source ITC-Scrape/bin/activate  
cd ITC-Scrape   
pip install -r requirements.txt
```

#### Command Line
This scraping utility can be manipulated via the following command line arguments:

1. ```--days``` with default of ```14```
2.  ```--search_type``` with default of both ```'forecast', 'historical'```
3.  ```--filename``` with default of ```ITC-Scrape/Cities/city_list.xlsx```**


#### Examples:

1. For historical weather data spanning two days
 ```
 %  python3 main.py --days=2 --search_type="historical"
 ```
2. For both historical and forecast weather data spanning 14 days, from a file of choice.
 ```
 %  python3 main.py --filename="path/to/file"
 ```
 **NOTE**<br>
   >This file of choice passed as ```--filename```argument must:
   > 1. be stored in the ```Cities``` directory 
   > 2. contain a```city``` column and a ```country``` column as headers in the first row 

All collected weather data is output into the Database 
in the corresponding table, according to arguments passed in via the CLI.

****NOTE**
>filepath *ITC-Scrape/Cities/city_list.xlsx* is set in ```cfg.FILENAME``` variable in ```config.py``` 



##  Databasing

The installation of this scraping utility provides a relational database which includes three tables:

1. Locations
2. Forecasts 
3. Historical Data

__Locations:__

```
Id: int NOT NULL AUTO_INCREMENT, PRIMARY KEY

Name: varchar(255), Location name

BBC_Id: varchar(10) NOT NULL, Location number in the url
```

__Historical:__

```
Id: int, NOT NULL, AUTO_INCREMENT, PRIMARY KEY

Scrape_Date: date, Date of the scrape

Date: date, The day which the data scraped

Hour: int, The hour in the specific day

Temperature_C: int, Temperature in celsius

Weather: varchar(30), General description of tha day conditions

Wind_Speed_Kph: int, Wind speed in kilometer per hour

Percent_Humidity: int, Percent of humidity

Pressure_Mb: int, Air pressure in millibar

Visibility_Km: int, Visibility conditions in kilometer.

Location_Id: int, FOREIGN KEY, REFERENCES (Locations.Id)
```

__Forecasts:__

```
Id: int, NOT NULL, AUTO_INCREMENT, PRIMARY KEY

Scrape_Date: date, Date of the scrape

Date: date, The day which the data scraped

Hour: int, The hour in the specific day

Temperature_C: int, Temperature in celsius

Chance_of_Rain: int, Chance percent of precipitation

Wind_Speed_Kph: int, Wind speed in kilometer per hour

Percent_Humidity: int, Percent of humidity

Pressure_Mb: int, Air pressure in millibar

Feels_Like_C: int, The feels like temperature in celsius

Location_Id: int, FOREIGN KEY, REFERENCES (Locations.Id)
```


__Pollution:__

```
Location_Id: int, NOT NULL, FOREIGN KEY REFERENCES (Locations.Id)

Date: date, Date of the scrape

Time: int, The hour in the specific day

CO: float, Сoncentration of CO (Carbon monoxide), μg/m3

NO: float, Сoncentration of NO (Nitrogen monoxide), μg/m3

NO2: float, Сoncentration of NO2 (Nitrogen dioxide), μg/m3

O3: float, Сoncentration of O3 (Ozone), μg/m3

SO2: float,	Сoncentration of SO2 (Sulphur dioxide), μg/m3

NH3: float, Сoncentration of NH3 (Ammonia), μg/m3

PM2_5: float, Сoncentration of PM2.5, (Fine Particulate matter), ug/m3

PM10 float, Сoncentration of PM10 (Coarse particulate matter), μg/m3
```

 __ERD Diagram__ : 
 
 ![alt text](https://github.com/tiguere/ITC-Scrape/blob/master/Database/weather.png?raw=true)

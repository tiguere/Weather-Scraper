ITC-Scrape - BBC Weather Scraper
===

A scraping utility which downloads high-resolution weather data from BBC's public weather stations around the world.

The list of cities are read from city_list.xlsx; each city weather data is scraped for a 14 day range and an hourly resolution. The collected weather data outputs into a CSV called test.csv.

### Requirements ###

Python 3 or higher

Selenium Driver -- Please see https://www.selenium.dev/downloads/

Pandas

Requests

Beautiful Soup

```python
git clone https://github.com/tiguere/ITC-Scrape.git  
virtualenv ITC-Scrape  
source ITC-Scrape/bin/activate  
cd ITC-Scrape   
pip install -r requirements.txt
```

### Contribution guidelines ###


### Who do I talk to? ###

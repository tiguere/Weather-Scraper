"""
scraping project - part 2
insert historical data module
"""


def get_location_id(cur, city_name):
    cur.execute(f"SELECT Id FROM weather.Locations WHERE Name = '{city_name}'")
    results = cur.fetchall()
    try:
        first_result = results[0]
        city_id = first_result[0]
        return city_id
    except IndexError as err:
        print(f"{err}: for results set: {results}")


import requests
import mysql.connector
from datetime import datetime
from Database.database_design import connection
from geopy.geocoders import Nominatim
import logging
import config as cfg


def get_city_pollution(city, country, token=cfg.API_TOKEN, url=cfg.API_ENDPOINT):
    """return air pollution data by request from API
    according to specify location"""

    geolocator = Nominatim(user_agent="request_api", timeout=10)
    loc = geolocator.geocode(city + ','+country)
    try:
        response = requests.get(f"{url}lat={loc.latitude}&lon={loc.longitude}&appid={token}")
        logging.info(f'city:{city},response status:{response.status_code}')
    except Exception as e:
      logging.info(f"{e},city:{city},doesn't have available pollution data")
    else:
        data = response.json()['list'][0]['components']
        d_time = datetime.utcfromtimestamp(response.json()['list'][0]['dt'])
        date = d_time.date().strftime('%Y-%m-%d')
        time = d_time.time().strftime('%H:%M')
        co = data['co']
        no = data['no']
        no2 = data['no2']
        o3 = data['o3']
        so2 = data['so2']
        pm2_5 = data['pm2_5']
        pm10 = data['pm10']
        nh3 = data['nh3']

        return [city, date, time, co, no, no2, o3, so2, nh3, pm2_5, pm10]


def insert_pollution(data, city):
    """insert pollution data to the pollution table
    according to location"""

    con = connection()
    cursor = con.cursor()
    cursor.execute(f"select Id from weather.Locations where Name ='{city}'")
    id_to_insert = cursor.fetchone()[0]

    data.insert(0, id_to_insert)
    check = """select Pollution.location,Pollution.date,Pollution.time
                   from weather.Pollution where Pollution.location=%s
                   and weather.Pollution.date=%s
                   and weather.Pollution.time=%s"""
    values = (data[1],data[2],data[3])
    try:
        cursor.execute(check,values)
        res = cursor.fetchall()
    except Exception as e:
        logging.info(f'{e}')
    else:
        if not res:
            query = ("""INSERT INTO weather.Pollution (Location_Id,location,date,time,CO,NO,NO2,O3,SO2,NH3,PM2_5,PM10)
                        VALUES (%(Location_Id)s,
                                %(location)s,
                                %(date)s,
                                %(time)s,
                                %(CO)s,
                                %(NO)s,
                                %(NO2)s,
                                %(O3)s,
                                %(SO2)s,
                                %(NH3)s,
                                %(PM2_5)s,
                                %(PM10)s)
                        """)
            val = {'Location_Id': data[0],
                   'location': data[1],
                   'date': data[2],
                   'time': data[3],
                   'CO': data[4],
                   'NO': data[5],
                   'NO2': data[6],
                   'O3': data[7],
                   'SO2': data[8],
                   'NH3': data[9],
                   'PM2_5': data[10],
                   'PM10': data[11]}
            try:
                cursor.execute(query,val)
                print(f"Pollution data INSERTED FOR: {city} on {data[2]} at {data[3]}")
            except mysql.connector.Error as err:
                logging.error(f"{err}: failed to insert for city: \n{city}.")
                exit(1)
            else:
                con.commit()
                cursor.close()
                con.close()




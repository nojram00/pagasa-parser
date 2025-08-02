from bs4 import BeautifulSoup
import requests
from db.models.forecast_conditions import ForecastConditions
from db.models.wind_and_coastal_waters import WindAndCoastalWaters
from db.setup_db import setup_db
from datetime import datetime

"""

This will be a cron job and runs every 6 hours.
This will fetch the data from the pagasa website and save to database.

"""

response = requests.get('https://pagasa.dost.gov.ph/weather#daily-weather-forecast')
html = BeautifulSoup(response.text, 'html.parser')

tables = html.find_all('table')

def get_forecast_data(table_index):
    forecast_table = tables[table_index]
    forecast_headers = forecast_table.find_all('tr')[0].find_all('th')
    forecast_rows = forecast_table.find_all('tr')[1:]

    forecast_data = []

    for forecast_row in forecast_rows:
        data = {}
        forecast_cols = forecast_row.find_all(['td', 'th'])
        for index, forecast_header in enumerate(forecast_headers):
            header = forecast_header.text.strip()
            value = forecast_cols[index].text.strip()
            data[header] = value
        forecast_data.append(data)

    return forecast_data

# Parse Forecast Conditions:

forecast_conditions = get_forecast_data(0)
wind_and_coastal_waters = get_forecast_data(1)

# for forecast_header in forecast_headers:
#     print(forecast_header.text)

if __name__ == "__main__":
    setup_db()
    url = "https://weather-api-781h.onrender.com/forecast-conditions"


    for forecast_condition in forecast_conditions:
        fc = ForecastConditions(
            date=datetime.now(),
            caused_by=forecast_condition['Caused By'],
            impacts=forecast_condition['Impacts'],
            place=forecast_condition['Place'],
            weather_condition=forecast_condition['Weather Condition']
        )
        fc.save()   

        # response = requests.post(url, json={
        #     'date': datetime.now().isoformat(),
        #     'caused_by': forecast_condition['Caused By'],
        #     'impacts': forecast_condition['Impacts'],
        #     'place': forecast_condition['Place'],
        #     'weather_condition': forecast_condition['Weather Condition']
        # })

        # print(response.text)

    for wind_and_coastal_water in wind_and_coastal_waters:
        wac = WindAndCoastalWaters(
            date=datetime.now(),
            place=wind_and_coastal_water['Place'],
            speed=wind_and_coastal_water['Speed'],
            direction=wind_and_coastal_water['Direction'],
            coastal_water=wind_and_coastal_water['Coastal Water']
        )
        wac.save()

    
    # print("====================================")
    # pprint.pprint(wind_and_coastal_water)
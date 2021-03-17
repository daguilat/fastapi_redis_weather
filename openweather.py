import logging
import requests
import json
import random
import datetime
from redis_connect import redis_connect 

redis_instance = redis_connect()

API_KEY = '734cdaaaa3be72280d206ea4db789ee1'

# Function to get city weather from openweather API 
# Input: longitude: str, latitude: str
# Output: response: json object with the city weather info
# Author: Diego Águila
# Date: 15-03-2021
def openweather_city_weather(longitude: str, latitude: str):
   logging.info("Trying to get city weather")
   error = True
   while(error == True):
      if (random.random() < 0.1):
            logging.warn("How unfortunate! The API Request Failed, trying again...")              
            redis_instance.hset("api.errors", datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), "How unfortunate! The API Request Failed")
      else:
            error = False
   url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}'.format(latitude,longitude,API_KEY)
   response = requests.get(url).json()

   if response:
      return json.dumps(response)
   else:
      logging.warning("No results obtained from %s", url)
      return ''
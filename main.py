import logging
import logging.config
import json
import time

from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from redis_connect import redis_connect as redis_connect
from city_loader import load_cities as load_cities
from openweather import openweather_city_weather as openweather_city_weather


logging.config.fileConfig('logging.conf')
# create logger
logger = logging.getLogger('weather')

app = FastAPI()

#Connection to database
redis_instance = redis_connect()

#Loading cities
load_cities(redis_instance)

logger.info("Waiting websocket connections...")

#Websocket connection handler
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_data(self, data: any, websocket: WebSocket):
        await websocket.send_text(data)



manager = ConnectionManager()

# Function to get city weather from openweather API 
# Input: websocket: Websocket connection
# Output: response: json object with the city weather info
# Author: Diego Águila
# Date: 16-03-2021
@app.websocket("/weather")
async def get_city_weather(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            cities_string = await websocket.receive_text()
            cities = cities_string.split(",")
            weatherData = []
            print(cities)
            for city in cities:
                print(city)
                data = redis_instance.hgetall(city)
                lon = data["lon"]
                lat = data["lat"]
                cityWeather = openweather_city_weather(lon,lat)
                weatherData.append(cityWeather)
            weatherData = json.dumps(weatherData)
            await manager.send_data(weatherData, websocket)
            logger.info(f"Successfully sent weather info of cities")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        logger.info(f"Communication ended.")
import logging
import logging.config
import json
import asyncio
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

loop = asyncio.get_event_loop()

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

@app.websocket("/weather")
async def manage_requests(websocket: WebSocket):
    await manager.connect(websocket)
    data = json.loads(await websocket.receive_text())
    if data["route"] == "get_city_coords":
        loop.run_until_complete(await get_city_coords(websocket, data))
    elif data["route"] == "get_city_weather":
        loop.run_until_complete(await get_city_weather(websocket, data))
    #manager.disconnect(websocket)

# Function to get city coords from redis database 
# Input: websocket: Websocket connection
# Output: response: json object with the city coords
# Author: Diego Águila
# Date: 16-03-2021
# @app.websocket("/get_city_coords")
async def get_city_coords(websocket: WebSocket, data: json):
    try:
        while True:
            name = data["name"]
            logging.info("Trying to get %s city coords", name)
            data = redis_instance.hgetall(name)
            lon = data["lon"]
            lat = data["lat"]
            response = '{"opt":"1", "name": "' + name + '", "lon": "' + lon + '", "lat": "' + lat + '"}'
            await manager.send_data(response, websocket)
            logging.info(f"Successfully sent longitude: {lon} and latitude {lat} from {name}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Function to get city weather from openweather API 
# Input: websocket: Websocket connection
# Output: response: json object with the city weather info
# Author: Diego Águila
# Date: 16-03-2021
# @app.websocket("/get_city_weather")
async def get_city_weather(websocket: WebSocket, data: json):
    try:
        while True:
            data = await websocket.receive_text()
            lon = data["lon"]
            lat = data["lat"]
            response = openweather_city_weather(lon, lat)
            await manager.send_data(response, websocket)
            logger.info(f"Successfully sent weather info on longitude: {lon} and latitude: {lat}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"Communication ended.")

import logging

LON_SANTIAGO = -70.6483
LAT_SANTIAGO = -33.4569

LON_ZURICH  = 8.5307
LAT_ZURICH  = 47.3828

LON_AUCKLAND = 174.7833
LAT_AUCKLAND = -36.85

LON_SYDNEY  = 151.2073
LAT_SYDNEY  = -33.8679

LON_LONDON = -0.1257
LAT_LONDON = 51.5085

LON_GEORGIA = -83.5002
LAT_GEORGIA = 32.7504

# Function to load given city into redis database
# Input: city_name: str, city_lon: float, city_lat: float, redis_instance: Redis 
# Output: void
# Author: Diego Águila
# Date: 15-03-2021
def load_city(city_name, city_lon, city_lat, redis_instance):
    logging.info("Loading city: %s with longitude: %s and latitude: %s",city_name, city_lon, city_lat)
    redis_instance.hset(city_name, "lon", city_lon)
    redis_instance.hset(city_name, "lat", city_lat)

# Function to load five cities into redis database
# Input: redis_instance: Redis 
# Output: void
# Author: Diego Águila
# Date: 15-03-2021
def load_cities(redis_instance):
    logging.info("Loading cities info")
    load_city('Santiago', LON_SANTIAGO, LAT_SANTIAGO, redis_instance)
    load_city('Zúrich'  , LON_ZURICH  , LAT_ZURICH, redis_instance)
    load_city('Auckland', LON_AUCKLAND, LAT_AUCKLAND, redis_instance)
    load_city('London',   LON_LONDON,   LAT_LONDON, redis_instance)
    load_city('Georgia',  LON_GEORGIA,  LAT_GEORGIA, redis_instance)
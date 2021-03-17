import logging
import redis
import sys

def redis_connect() -> redis.client.Redis:
    logging.info("Trying to connect to database")
    try:
        client = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
            decode_responses=True
        )
        ping = client.ping()
        if ping is True:
            logging.info("Connection established successfully")
            return client
    except redis.AuthenticationError:
        print("AuthenticationError")
        logging.error("AuthenticationError: {}".format(redis.AuthenticationError))
        sys.exit(1)
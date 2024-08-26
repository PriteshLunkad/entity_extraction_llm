from mongoengine import connect, disconnect
from config.secrets import MONGO_DB_CONFIG
from loguru import logger


def connect_to_mongo():
    """
    Establish a connection to the MongoDB database using the configuration
    provided in MONGO_DB_CONFIG. Logs a message indicating whether the
    connection was successful or raises an error if the connection fails.
    """
    try:
        # Establish a connection to MongoDB
        connect(**MONGO_DB_CONFIG)
        logger.info("Connection to MongoDB successful")
    except Exception as e:
        # Raise a ConnectionError if the connection fails
        raise ConnectionError("Could not connect to MongoDB") from e
    finally:
        # Disconnect from MongoDB
        disconnect()

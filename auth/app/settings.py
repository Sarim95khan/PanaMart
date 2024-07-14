from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()
    
DATABASE_URL = config(
    "DATABASE_URL", cast=Secret)

BOOTSTRAP_SERVER = config("BOOTSTRAP_SERVER", cast=str)
KAFKA_AUTH_TOPIC = config("KAFKA_AUTH_TOPIC", cast=str)
KAFKA_CONSUMER_GROUP_ID_FOR_AUTH = config("KAFKA_CONSUMER_GROUP_ID_FOR_AUTH", cast=str)


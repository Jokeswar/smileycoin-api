from pymongo import MongoClient
from pymongo.database import Database

from src import settings

client = MongoClient(
    f"mongodb://{settings.MONGO_ROOT_USERNAME}:{settings.MONGO_ROOT_PASSWORD}@{settings.MONGODB_HOST}:{settings.MONGODB_PORT}"
)


def get_database() -> Database:
    return client[settings.MONGODB_DATABASE]

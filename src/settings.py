import os

# MongoDB Config
MONGODB_HOST = os.environ.get("MONGODB_HOST", "localhost")
MONGODB_PORT = os.environ.get("MONGODB_PORT", "27017")
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "db")
MONGO_ROOT_USERNAME = os.environ.get("MONGO_ROOT_USERNAME", "admin")
MONGO_ROOT_PASSWORD = os.environ.get("MONGO_ROOT_PASSWORD", "secret")

import os

ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
SERVICE_NAME = "xxxxx"
GITHUB_USERNAME = "minhnt10" #for code document generation

SERVICE_GRAYLOG_IP = os.environ.get("SERVICE_GRAYLOG_IP", "103.137.4.92")
SERVICE_GRAYLOG_PORT = os.environ.get("SERVICE_GRAYLOG_PORT", 12201)
SERVICE_KNIGHTMARE_IP = os.environ.get("SERVICE_KNIGHTMARE_IP", "http://42.113.207.186:5123")

MONGO_URI = os.environ["MONGO_URI"]
MONGO_COLLECTION = os.environ["MONGO_COLLECTION"]

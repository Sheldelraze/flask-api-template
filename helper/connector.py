import pymongo
from pymongo import errors

import config
from helper import singleton


class MongoConnector(object, metaclass=singleton.Singleton):
    def __init__(self, mongo_uri=config.MONGO_URI, mongo_collection=config.MONGO_COLLECTION):
        self.client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
        self.mongodb = self.client.get_database(mongo_collection)

        #uncomment these line to perform health check on startup
        # try:
        #     self.client.admin.command("ismaster")
        # except (errors.ConnectionFailure, errors.ServerSelectionTimeoutError) as e:
        #     print("Fail! Server mongodb not available!, error = {}: {}".format(type(e).__name__, str(e)))
        #     exit()

    def get_connector(self):
        return self.mongodb

    def get_mongo_client(self):
        return self.client

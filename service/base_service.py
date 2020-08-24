import typing

import config
from helper import connector, singleton


class BaseService(object, metaclass=singleton.Singleton):
    def __init__(self):
        mongo_connector = connector.MongoConnector()
        self.mongodb = mongo_connector.get_connector()

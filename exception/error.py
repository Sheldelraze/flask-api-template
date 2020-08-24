from enum import Enum


class ErrorCode(Enum):
    BASE = 10000
    GENERAL = BASE + 1
    INVALID_REQUEST = BASE + 2


class Error(Exception):
    """Base class for other exceptions"""

    def __init__(self, data={}):
        self.data = data
        self.code = ErrorCode.GENERAL.value
        self.message = ""
        self.status_code = 500


class InvalidRequest(Error):
    def __init__(self, data={}):
        super(InvalidRequest, self).__init__(data)
        self.message = "Invalid request!"
        self.code = ErrorCode.INVALID_REQUEST.value
        self.status_code = 400

# -*- coding: utf-8 -*-
"""
Service

Developers:
Minh Nguyễn

Description:
Service for sample API
"""


from exception import error
from helper import common_util, connector, singleton
from service import base_service


class SampleService(base_service.BaseService, metaclass=singleton.Singleton):
    """
    Class used for processing exam API service
    """

    def __init__(self):
        super().__init__()

    @common_util.timing
    def get_sample(self, user_id: str, event_timestamp: float, params_one: str, params_two: int) -> dict:
        """
        Function used to extract parameters from a function docstring.

        Parameters
        ----------
        user_id : str
            unique itentifier for user
        event_timestamp: float
            current UNIX timestamp
        params_one : str
            A random string for demonstation purpose
        params_two : int
            A random integer for demonstation purpose

        Returns
        -------
        params : dict
            You can automatically build and test your application if you enable Auto DevOps for this project.
        """
        return {"question": "What is love?"}

    @common_util.timing
    def post_sample(self, user_id: str, event_timestamp: float, params_three: int, params_four: int) -> dict:
        """
        Function used to extract parameters from a function docstring.

        Parameters
        ----------
        user_id : str
            unique itentifier for user
        event_timestamp: float
            current UNIX timestamp
        params_four : str
            A random string for demonstation purpose
        params_three : int
            A random integer for demonstation purpose

        Returns
        -------
        params : dict
            Otherwise it is recommended you start with one of the options below. 
        """
        return {"answer": "Baby don't hurt me..."}

    # TODO: Delete this
    @common_util.timing
    def get_unknown_error(self):
        raise ValueError("Dont hurt me...")

    # TODO: Delete this
    @common_util.timing
    def get_custom_error(self):
        raise error.Error(data="No more")

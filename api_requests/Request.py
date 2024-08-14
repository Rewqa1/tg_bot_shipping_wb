import json
import os

import requests


class EmptyResponseError(Exception):
    """Raised when the response is empty"""
    pass

class ResponseError(Exception):
    """Raised when the response status code is not 200"""
    pass
class Request:
    def __init__(self, token: str, url: str, headers: dict | None, params: dict | None):
        self.token = token
        self.url = url
        self.headers = headers
        self.params = params

    def get_data(self):
        response = requests.get(url=self.url, headers=self.headers, params=self.params)
        return self.__check_response(response)

    def post_data(self):
        response = requests.post(url=self.url, headers=self.headers, data=json.dumps(self.params))
        return self.__check_response(response)

    def __check_response(self, response):
        if response.status_code == 200:
            data = response.json()
            if data:
                return data
            else:
                raise EmptyResponseError('Empty response')

        else:
            raise ResponseError(f'Response status code: {response.status_code}: {response.text}')

class RequestWB(Request):
    def __init__(self, token: str, url: str, params):

        super().__init__(token=token, url=url, params=params, headers=None)

        self.headers = {'Authorization': self.token, 'Content-Type': 'application/json'}




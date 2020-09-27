from urllib import request as http
from urllib.error import HTTPError


class Service():
    def __init__(self):
        self._endpoint = r'https://front-test-pg.herokuapp.com'
        # todo: add headers (instance of Request class)

    def get(self, params):
        return http.urlopen(f'{self._endpoint}{params}')

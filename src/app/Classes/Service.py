from urllib import request as http


class Service():
    def __init__(self):
        self._endpoint = r'https://front-test-pg.herokuapp.com'
        # todo: add headers (instance of Request class)

    def GET(self, params=None):
        return http.urlopen(f'{self._endpoint}{params}')

from src.app.Classes import Service

import json
from urllib.error import HTTPError


class FileService(Service):
    def getEndpoint(self):
        return self._endpoint

    def getRequest(self, params=None):
        try:
            return self.GET(f'{params}')

        except HTTPError as err:
            if err.code == 404:
                return None

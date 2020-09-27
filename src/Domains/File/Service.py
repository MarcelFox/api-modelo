from src.app.Classes.superService import Service


class FileService(Service):
    def getEndpoint(self):
        return self._endpoint

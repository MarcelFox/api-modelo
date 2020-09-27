from src.app.Classes import Service


class FileService(Service):
    def getEndpoint(self):
        return self._endpoint

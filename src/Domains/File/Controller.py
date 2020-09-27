from flask import jsonify
from csv import DictReader

from .Service import FileService
from urllib.error import HTTPError


class FileController:
    def __init__(self):
        self._fileService = FileService()

    @staticmethod
    def mainPage():
        return jsonify({"status": 200, "message": "Main Success"})

    def checkNumbers(self, file):
        validLines = []
        for e in DictReader(file.splitlines(), delimiter=';'):
            if len(e["DDD"]) < 2:
                continue

            if int(e["CELULAR"][1]) < 6:
                continue

            try:
                self._fileService.get(f'/blacklist/{e["DDD"]}{e["CELULAR"]}')
            except HTTPError as err:
                if err.code == 404:
                    validLines.append(e)
        return jsonify(validLines)

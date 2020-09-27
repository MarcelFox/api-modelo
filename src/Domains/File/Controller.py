from flask import jsonify
from csv import DictReader

from .Service import FileService
from urllib.error import HTTPError


class FileController:
    def __init__(self):
        self._fileService = FileService()
    
    def mainPage(self):
        return jsonify({"status": 200, "message": "Main Success"})

    def checkNumbers(self, file):
        validLines = []
        for e in DictReader(file.splitlines(), delimiter=';'):
            if int(e["CELULAR"][0]) != 9:
                print(e["CELULAR"])
                continue

            if len(e["DDD"]) < 2 or len(e["CELULAR"]) != 9:
                continue

            if int(e["CELULAR"][1]) < 6:
                continue

            print(e["OPERADORA"])
            e["BROKER"] = self.__getBroker(e["OPERADORA"])

            try:
                self._fileService.get(f'/blacklist/{e["DDD"]}{e["CELULAR"]}')
            except HTTPError as err:
                if err.code == 404:
                    validLines.append(f'{e["IDMENSAGEM"]};{e["BROKER"]}')
        return jsonify(validLines)

    def __getBroker(self, op):
        print(op)
        return {
            "VIVO": 1,
            "TIM": 1,
            "CLARO": 2,
            "OI": 2,
            "NEXTEL": 3
        }.get(op, None)

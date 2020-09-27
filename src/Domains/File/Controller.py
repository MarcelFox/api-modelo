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
        numbersChecked = self.__numValidation(file)
        validLines = self.__requestNumbers(numbersChecked)

        return jsonify(validLines)

    def __numValidation(self, payload: dict):
        validNumbers = []
        for data in DictReader(payload.splitlines(), delimiter=';'):
            if int(data["CELULAR"][0]) != 9:
                continue

            if len(data["DDD"]) < 2 or len(data["CELULAR"]) != 9:
                continue

            if int(data["CELULAR"][1]) < 6:
                continue

            data["BROKER"] = self.__getBroker(data["OPERADORA"])
            validNumbers.append(data)
        return validNumbers

    def __getBroker(self, op: str):
        print(op)
        return {
            "VIVO": 1,
            "TIM": 1,
            "CLARO": 2,
            "OI": 2,
            "NEXTEL": 3
        }.get(op, None)

    def __requestNumbers(self, payload: list):
        validLines = []
        for data in payload:
            try:
                self._fileService.get(
                    f'/blacklist/{data["DDD"]}{data["CELULAR"]}')
            except HTTPError as err:
                if err.code == 404:
                    validLines.append(f'{data["IDMENSAGEM"]};{data["BROKER"]}')
        return validLines

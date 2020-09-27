import json
from datetime import datetime
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

    def checkNumbersFast(self, file):
        data = self.__numValidation(file)
        numbersChecked = [
            f'{e["DDD"]}{e["CELULAR"]}' for e in data]

        # get available blacklist:
        response = self._fileService.getRequest(
            r'/blacklist').read().decode('utf8')

        blacklist = [e["phone"] for e in json.loads(response)]
        whiteNumbers = [num for num in numbersChecked if num not in blacklist]

        validNumbers = [
            f'{e["IDMENSAGEM"]};{e["BROKER"]}'
            for e in data
            if f'{e["DDD"]}{e["CELULAR"]}' in whiteNumbers
        ]

        return jsonify(validNumbers)

    def __numValidation(self, payload):
        validNumbers = []
        for data in DictReader(payload.splitlines(), delimiter=';'):
            if int(data["DDD"]) == 11:
                continue

            if(len(data["MENSAGEM"]) >= 140):
                continue

            if int(data["CELULAR"][0]) != 9:
                continue

            if len(data["DDD"]) < 2 or len(data["CELULAR"]) != 9:
                continue

            if int(data["CELULAR"][1]) < 6:
                continue

            if (self.timeDiff(data["HORARIO_ENVIO"])):
                continue

            data["BROKER"] = self.__getBroker(data["OPERADORA"])
            validNumbers.append(data)
        return validNumbers

    def __getBroker(self, op):
        return {
            "VIVO": 1,
            "TIM": 1,
            "CLARO": 2,
            "OI": 2,
            "NEXTEL": 3
        }.get(op, None)

    def __requestNumbers(self, payload):
        validLines = []
        for data in payload:
            blacklisted = self._fileService.getRequest(
                f'/blacklist/{data["DDD"]}{data["CELULAR"]}')

            if not blacklisted:
                validLines.append(f'{data["IDMENSAGEM"]};{data["BROKER"]}')
        return validLines

    @staticmethod
    def timeDiff(hour1, hour2="19:59:59"):
        timeFormat = "%H:%M:%S"
        t1 = datetime.strptime(hour1, timeFormat)
        t2 = datetime.strptime(hour2, timeFormat)
        return (t2 < t1)

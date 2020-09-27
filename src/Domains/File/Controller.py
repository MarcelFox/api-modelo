import json
import functools
from datetime import datetime
from flask import jsonify
from csv import DictReader

from src.app.Utils import ddd_list
from .Service import FileService
from urllib.error import HTTPError


class FileController:
    def __init__(self):
        self._fileService = FileService()

    def mainPage(self):
        return jsonify({"status": 200, "message": "Main Success"})

    def checkNumbers(self, file):
        numbersChecked = self.__numValidation(file)
        validMessages = self.__requestNumbers(numbersChecked)
        return jsonify(validMessages)

    def checkNumbersFast(self, file):
        data = functools.reduce(self.callback, self.__numValidation(file), [])
        numbersChecked = [
            f'{e["DDD"]}{e["CELULAR"]}' for e in data]

        # get available blacklist:
        response = self._fileService.getRequest(
            r'/blacklist').read().decode('utf8')

        blacklist = [e["phone"] for e in json.loads(response)]
        validLines = [num for num in numbersChecked if num not in blacklist]

        validMessages = [
            f'{e["IDMENSAGEM"]};{e["BROKER"]}'
            for e in data
            if f'{e["DDD"]}{e["CELULAR"]}' in validLines
        ]

        return jsonify(validMessages)

    def __numValidation(self, payload):
        validNumbers = []
        dddArr = [e["DDD"] for e in ddd_list]

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

            if int(data["DDD"]) not in dddArr:
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

    def callback(self, acc, value):
        acc.append(value)
        if len(acc) > 1:
            oldTime = f'{acc[-2]["HORARIO_ENVIO"]}'
            newTime = f'{value["HORARIO_ENVIO"]}'
            oldVal = f'{acc[-2]["DDD"]}{acc[-2]["CELULAR"]}'
            newVal = f'{value["DDD"]}{value["CELULAR"]}'
            if oldVal == newVal:
                val = -1 if self.timeDiff(
                    newTime, oldTime) else -2
                del acc[val]
        return acc

    @staticmethod
    def timeDiff(hour1, hour2="19:59:59"):
        timeFormat = "%H:%M:%S"
        t1 = datetime.strptime(hour1, timeFormat)
        t2 = datetime.strptime(hour2, timeFormat)
        return (t2 < t1)

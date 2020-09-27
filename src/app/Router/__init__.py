
from flask import jsonify, request
from flask import current_app as app


from src.Domains.File.Controller import FileController

import json
from csv import DictReader

fileController = FileController()


@app.route('/', methods=['GET'])
def default():
    return jsonify({"status": 200, "message": "api-modelo v1.0"})


@app.route('/main', methods=['GET'])
def main():
    return fileController.mainPage()


@app.route('/', methods=['POST'])
def checkCsv():
    output = request.files['file'].read().decode('utf8')
    return fileController.checkNumbers(output)

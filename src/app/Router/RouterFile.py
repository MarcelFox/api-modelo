
from flask import Blueprint, jsonify, request
from flask import current_app as app


from src.Domains import FileController

from csv import DictReader

fileController = FileController()
file_urls = Blueprint('RouterFile', __name__)


@file_urls.route('/', methods=['GET'])
def default():
    return jsonify({"status": 200, "message": "api-modelo v1.0"})


@file_urls.route('/main', methods=['GET'])
def main():
    return fileController.mainPage()


@file_urls.route('/checkCsv', methods=['POST'])
def checkCsv():
    output = request.files['file'].read().decode('utf8')
    return fileController.checkNumbers(output)


@file_urls.route('/checkCsvFast', methods=['POST'])
def checkCsvFast():
    output = request.files['file'].read().decode('utf8')
    return fileController.checkNumbersFast(output)

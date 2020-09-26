
from flask import jsonify
from flask import current_app as app
from src.Domains.File.file_controller import main_page


@app.route('/', methods=['GET'])
def default():
    return jsonify({"status": 200, "message": "api-modelo v1.0"})


@app.route('/main', methods=['GET'])
def main():
    return main_page()

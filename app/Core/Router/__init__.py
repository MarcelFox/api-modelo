
from flask import jsonify
from flask import current_app as app


@app.route('/', methods=['GET'])
def main_page():
    return jsonify({"status": 200, "message": "Success"})

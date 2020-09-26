from flask import jsonify


def main_page():
    return jsonify({"status": 200, "message": "Success"})


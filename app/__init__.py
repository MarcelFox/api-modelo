from flask import Flask
app = Flask(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    with app.app_context():
        import Router
        return app

from flask import Flask


def create_app():
    app = Flask(__name__)
    # app.config.from_object('config')

    with app.app_context():
        from src.app.Router import file_urls
        app.register_blueprint(file_urls)
        return app

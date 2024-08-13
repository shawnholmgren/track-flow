from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    from . import routes
    app.register_blueprint(routes.bp)

    return app


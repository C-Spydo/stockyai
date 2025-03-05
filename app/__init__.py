from .error_handler import register_error_handlers
from .controllers import routes_blueprint
from dotenv import load_dotenv
from flask_cors import CORS
from .config import Config
from .extensions import *
from .constants import *
from flask import Flask
from flask_restx import Api

load_dotenv()

def create_app(config_class=Config):

    app = Flask(__name__)

    app.config.from_object(config_class)

    CORS(app)

    # api = Api(app,version="1.0", title="StockyAPi", description="StockyAPi API", doc="/swagger/")


    register_blueprints(app)

    initialize_extensions(app)

    return app


def initialize_extensions(app):
    database.init_app(app)

    db_migration.init_app(app, database)


def register_blueprints(app):
    # api.init_app(routes_blueprint)
    app.register_blueprint(routes_blueprint, url_prefix="/api")




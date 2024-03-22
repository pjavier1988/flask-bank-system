from flask import Flask
from dependency_injector.wiring import wire
from flask_restx import Api

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config.config import Config
from app.config.logging import configure_logging
from .containers import Container
from .database import db
from app.namespaces.user import user_ns
from flask_cors import CORS

migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(config_class)
    
    api = Api(app, version='1.0', title='My API', description='A simple API')

    db.init_app(app)
    CORS(app)
    container = Container()
    container.config.from_dict(app.config)
    container.init_resources()
    container.wire(modules=["app.apis.users.routes",
                            "app.apis.transactions.routes",
                            "app.apis.accounts.routes",
                            "app.apis.auth.routes"
                            ])
    jwt = JWTManager(app)
    from app.apis.users import users_bp
    from app.apis.transactions import transactions_bp
    from app.apis.accounts import accounts_bp
    from app.apis.auth import auth_bp
    app.register_blueprint(users_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(auth_bp)
    migrate.init_app(app, db)
    api.add_namespace(user_ns)
    configure_logging(app)
    return app

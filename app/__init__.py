import os
import bcrypt
import logging
from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate


db = SQLAlchemy()
bootstrap = Bootstrap5()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "authentication.log_in_user"
login_manager.session_protection = "strong"

def create_app(config_type):
    app = Flask(__name__)
    configuration = os.path.join(os.getcwd(), "config", config_type + ".py")
    app.config.from_pyfile(configuration)
    configure_logging(app)
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    from app.auth import authentication
    app.register_blueprint(authentication)
    from app.products import products
    app.register_blueprint(products, url_prefix='/products')
    migrate = Migrate(app, db)
    return app

def configure_logging(app):
    del app.logger.handlers[:]
    # add logger using sqlalchemy
    # loggers = [app.logger, logging.getLogger('sqlalchemy')]
    loggers = [app.logger, ]
    handlers = []
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_formatter())

    if (app.config['FLASK_ENV'] == 'development'):
        console_handler.setLevel(logging.DEBUG)
        handlers.append(console_handler)
    elif app.config['FLASK_ENV'] == 'production':
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)

    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)

def verbose_formatter():
    return logging.Formatter('[%(asctime)s.%(msecs)d] | %(levelname)s | [%(name)s.%(funcName)s:%(lineno)d] %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

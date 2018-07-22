#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import  Bootstrap
from flask_moment import Moment
from flask_login import LoginManager
from config import config


bootstrap = Bootstrap()
monent = Moment()
db = SQLAlchemy()


login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    monent.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    from app.api_1_0 import api
    api.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .files import files as files_blueprint
    app.register_blueprint(files_blueprint, url_prefix="/files")

    from .posts import posts as posts_blueprint
    app.register_blueprint(posts_blueprint, url_prefix="/posts")

    return app














'''
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
'''
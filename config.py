#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')
    ALLOWED_EXTENSIONS = ['.jpg','.jpge','.png','.gif']
    MAX_CONTENT_LENGTH = 1024*1024*64 #64兆
    UPLOAD_FOLDED = os.getcwd()+'\\img'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/bank?charset=utf8'

class TestingConfig(Config):
    pass

class ProductionConfig(Config):
    pass

config = {
        'development':DevelopmentConfig,
        'default':DevelopmentConfig
        }
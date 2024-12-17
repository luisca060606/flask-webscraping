# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
load_dotenv()
FLASK_ENV = 'development'
FLASK_DEBUG = True
DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False
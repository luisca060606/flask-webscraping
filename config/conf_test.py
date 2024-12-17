# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
load_dotenv()
FLASK_ENV = 'development'
FLASK_DEBUG = True
DEBUG = True
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False
# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
load_dotenv()
FLASK_ENV = 'production'
FLASK_DEBUG = False
DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY')
# connect sqlite db
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
# connect postgresdb, before install psycopg2
# SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost:5432/db_name'
SQLALCHEMY_TRACK_MODIFICATIONS = False
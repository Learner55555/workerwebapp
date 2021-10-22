import os
SECRET_KEY = os.urandom(32)

DB_HOST = 'localhost:5432'
DB_USER = 'postgres'
DB_PASSWORD = '235689'
DB_NAME = 'it_project'

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)

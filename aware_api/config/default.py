import os

ENV = 'production'
DB_NAME = 'awareDB'
COLL_NAME = 'data'
DB_URI = os.getenv('DB_URI', 'not_defined')
DB_KEY = os.getenv('DB_KEY', 'not_defined')

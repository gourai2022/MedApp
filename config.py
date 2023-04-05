import os
from sqlalchemy import create_engine
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://'
SQLALCHEMY_TRACK_MODIFICATIONS = False
#secret_key = 'super secret key'
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=10, max_overflow=20)
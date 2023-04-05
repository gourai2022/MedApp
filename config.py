import os
from sqlalchemy import create_engine
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgres://medapp_user:2pljZnIaf1VAJO4gR0UjS7nqlKtbBlJO@dpg-cgmfsvbhp8ua8vpqebqg-a/medapp'
SQLALCHEMY_TRACK_MODIFICATIONS = False
#secret_key = 'super secret key'
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=10, max_overflow=20)
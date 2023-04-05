import os
from sqlalchemy import create_engine
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

database_name = "postgres_deployment_medapp"
#database_path = 'postgresql://postgres_deployment_medapp_user:EhRLLkptvFgJPnNmW6ezO9CoDGlkQZOw@dpg-cgmqgbrhp8ua8vs49q30-a/postgres_deployment_medapp'
database_path = "postgresql:///{}".format(database_name)
database_path = os.environ['DATABASE_URL']

# Connect to the database
SQLALCHEMY_DATABASE_URI = database_path
SQLALCHEMY_TRACK_MODIFICATIONS = False
#secret_key = 'super secret key'
engine = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=10, max_overflow=20)
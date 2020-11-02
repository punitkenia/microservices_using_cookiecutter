# Load the production settings that we will overwrite as needed in our user1 settings file.
from micro_api.config.production import *

# TODO
# Set a dummy secret key for local
SECRET_KEY = 'so=@6uf8p*wo=5*-foze2_s&cd+))86me5pzpx8)#9!bgbgg@6'

# Set DEBUG to true for local
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0']
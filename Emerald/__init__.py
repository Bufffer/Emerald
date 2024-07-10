from flask import Flask
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from Emerald import models

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
    
app.config["SECRET_KEY"] = SECRET_KEY

from Emerald import routes

from flask import Flask, render_template
from pymongo import MongoClient

import json
import pandas as pd
import csv
import os

mongo_client = MongoClient("mongodb+srv://gunganit:mongoDBGT@femadataset-hpenl.mongodb.net/test") 
db = mongo_client.fema

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

if __name__ == "__main__":
    app.run()
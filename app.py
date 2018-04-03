from flask import Flask, render_template, request
from datetime import datetime
from pymongo import MongoClient

import json
import pandas as pd
import csv
import os

mongo_client = MongoClient("mongodb+srv://gunganit:mongoDBGT@femadataset-hpenl.mongodb.net/test") 
db = mongo_client.fema

app = Flask(__name__)

@app.route('/')
def index():
    disaster_types = db.disasters_declarations_data.distinct("incidentType")
    return render_template("index.html", t=disaster_types)

@app.route('/', methods=['POST'])
def inputs_form_submit():
    disaster = request.form['disaster']
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    start = datetime.strptime(startDate, "%Y-%m-%d")
    end = datetime.strptime(endDate, "%Y-%m-%d")
    print("startDateObj: " , start)
    print("endDateObj: ", end)

    states = db.disasters_declarations_data.distinct("state", { "incidentBeginDate": { "$gte": start }, "incidentEndDate": { "$lte": end }, "incidentType": disaster})
    print("states", states)
    return "OK"

if __name__ == "__main__":
    app.run()
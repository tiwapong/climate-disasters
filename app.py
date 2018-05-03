from flask import Flask, render_template, request
from datetime import datetime
from pymongo import MongoClient

import json
import os

MONGO_URL = os.environ.get('PROD_MONGODB')
client = MongoClient(MONGO_URL)
# mongo_client = MongoClient("mongodb+srv://gunganit:mongoDBGT@femadataset-hpenl.mongodb.net/test") 
db = client.fema

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
    states = db.disasters_declarations_data.distinct("state", { "incidentBeginDate": { "$gte": start }, "incidentEndDate": { "$lte": end }, "incidentType": disaster})

    states_list = []
    for state_abr in states:
        st = get_state_name(state_abr)
        states_list.append(st)
    return parse_geoJSON(states_list)

def parse_geoJSON(states_list):
    data = json.load(open('us-states.json'))
    features = data['features']

    filtered_features = []
    for feature in features:
        if feature['properties']['name'] in states_list:
            filtered_features.append(feature)
    filtered_geojson = {}
    filtered_geojson['type'] = 'FeatureCollection'
    filtered_geojson['features'] = filtered_features

    return json.dumps(filtered_geojson)

def get_state_name(state_abr):
    states = [
        ['Alabama', 'AL'],
        ['Alaska', 'AK'],
        ['American Samoa', 'AS'],
        ['Arizona', 'AZ'],
        ['Arkansas', 'AR'],
        ['Armed Forces Americas', 'AA'],
        ['Armed Forces Europe', 'AE'],
        ['Armed Forces Pacific', 'AP'],
        ['California', 'CA'],
        ['Colorado', 'CO'],
        ['Connecticut', 'CT'],
        ['Delaware', 'DE'],
        ['District Of Columbia', 'DC'],
        ['Florida', 'FL'],
        ['Georgia', 'GA'],
        ['Guam', 'GU'],
        ['Hawaii', 'HI'],
        ['Idaho', 'ID'],
        ['Illinois', 'IL'],
        ['Indiana', 'IN'],
        ['Iowa', 'IA'],
        ['Kansas', 'KS'],
        ['Kentucky', 'KY'],
        ['Louisiana', 'LA'],
        ['Maine', 'ME'],
        ['Marshall Islands', 'MH'],
        ['Maryland', 'MD'],
        ['Massachusetts', 'MA'],
        ['Michigan', 'MI'],
        ['Minnesota', 'MN'],
        ['Mississippi', 'MS'],
        ['Missouri', 'MO'],
        ['Montana', 'MT'],
        ['Nebraska', 'NE'],
        ['Nevada', 'NV'],
        ['New Hampshire', 'NH'],
        ['New Jersey', 'NJ'],
        ['New Mexico', 'NM'],
        ['New York', 'NY'],
        ['North Carolina', 'NC'],
        ['North Dakota', 'ND'],
        ['Northern Mariana Islands', 'NP'],
        ['Ohio', 'OH'],
        ['Oklahoma', 'OK'],
        ['Oregon', 'OR'],
        ['Pennsylvania', 'PA'],
        ['Puerto Rico', 'PR'],
        ['Rhode Island', 'RI'],
        ['South Carolina', 'SC'],
        ['South Dakota', 'SD'],
        ['Tennessee', 'TN'],
        ['Texas', 'TX'],
        ['US Virgin Islands', 'VI'],
        ['Utah', 'UT'],
        ['Vermont', 'VT'],
        ['Virginia', 'VA'],
        ['Washington', 'WA'],
        ['West Virginia', 'WV'],
        ['Wisconsin', 'WI'],
        ['Wyoming', 'WY'],
    ]
    
    for st in states:
        if(st[1] == state_abr):
            return st[0]
    return 

@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
	response.headers.add('Access-Control-Allow-Credentials', 'true')
	return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(host='0.0.0.0')
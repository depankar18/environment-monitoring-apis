from flask import Flask, json
from flask_pymongo import PyMongo
from datetime import datetime
import time, calendar
from bson.json_util import dumps
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app)
app.config['MONGO_URI'] = "mongodb+srv://depankar_1:PR2bPFzLZcD716qr@cluster1.dcz0z.mongodb.net/database_2?retryWrites=false&w=majority"
mongo = PyMongo(app)
w_d=mongo.db.weather_crawler

@app.route("/get-all-weather-data", methods = ['GET', 'POST'])
def all_weather_data():
    data_list = list(w_d.find())
    json_data = dumps(data_list)
    return json_data

@app.route("/get-weather-data/<date_tmp>", methods = ['GET', 'POST'])
@cross_origin()
def weather_data_datewise(date_tmp):
    pattern='%Y-%m-%d'
    unix_date=int(calendar.timegm(time.strptime(date_tmp, pattern)))
    data=[]
    for i in range(0,24):
        tmp=w_d.find_one({'date_time_utc':datetime.utcfromtimestamp((i*3600+unix_date))})
        if tmp == None:
            response = app.response_class(
            response=json.dumps(data),
            status=404,
            mimetype='application/json')
            return response
        del tmp['_id']
        tmp['date_time_utc']=int(i*3600+unix_date)
        data.append(tmp)

    response = app.response_class(
    response=json.dumps(data),
    status=200,
    mimetype='application/json')

    return response

if __name__=="__main__":
    app.run(host="0.0.0.0", port=8000)
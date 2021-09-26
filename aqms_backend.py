from flask import Flask, json
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['MONGO_URI'] = "mongodb+srv://depankar_2:10oLgmqgdAWCN2wZ@cluster2.wnjrs.mongodb.net/database_1?retryWrites=false&w=majority"
mongo = PyMongo(app)
aqms_d=mongo.db.aqms_crawler

@app.route("/get-all-aqms-data", methods = ['GET', 'POST'])
def all_aqms_data():
    data_list = list(aqms_d.find())
    json_data = dumps(data_list)
    return json_data

@app.route("/get-aqms-data/<date_tmp>", methods = ['GET', 'POST'])
@cross_origin()
def aqms_data_datewise(date_tmp):
    data=[]
    tmp=aqms_d.find({'date_time_ist' : {'$regex' : '^'+date_tmp}})

    for i in tmp:
        del i['_id']
        data.append(i)

    if len(data) == 0:
        response = app.response_class(
        response=json.dumps(data),
        status=404,
        mimetype='application/json')
    else:
        response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json')

    return response

if __name__=="__main__":
    app.run(host="0.0.0.0", port=8010)
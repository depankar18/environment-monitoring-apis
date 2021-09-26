from flask import Flask, json
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['MONGO_URI'] = "mongodb+srv://depankar_3:RgKA1YLMJb4oVUtd@cluster3.zirzh.mongodb.net/database_3?retryWrites=false&w=majority"
mongo = PyMongo(app)
ems_d=mongo.db.ems_crawler_dv4

@app.route("/get-all-ems4-data", methods = ['GET', 'POST'])
def all_ems_data():
    data_list = list(ems_d.find())
    json_data = dumps(data_list)
    return json_data

@app.route("/get-ems4-data/<date_tmp>", methods = ['GET', 'POST'])
@cross_origin()
def ems_data_datewise(date_tmp):
    data=[]
    tmp=ems_d.find({'date' : {'$regex' : '^'+date_tmp}})

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
    app.run(host="0.0.0.0", port=8004)
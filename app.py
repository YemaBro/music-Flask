from flask import Flask, request
from flask_pymongo import PyMongo
from bson import json_util
from flask_cors import CORS
import config
import json

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/music'
mongo = PyMongo(app)
app.config.from_object(config)


# @app.route('/music/', methods=['GET'])
@app.route('/music', methods=['GET'])
def req_genre():
    if request.method == 'GET':
        genre = request.args.get('genre')
        page_size = int(request.args.get('pageSize'))
        page_num = int(request.args.get('pageNum'))
        singer = mongo.db.TaiheMusic.find({'$or': [{'genre': {'$regex': genre}}]}, {'_id': 0}).sort([('hot', -1)]).limit(page_size).skip(page_size*(page_num))
        total = mongo.db.TaiheMusic.find({'$or': [{'genre': {'$regex': genre}}]}, {'_id': 0}).count()
        singer_body = json.loads(json_util.dumps(singer))
        new_d = {'singer_body': singer_body, 'total': total}
        singer_json = json_util.dumps(new_d)
        return singer_json




if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run()

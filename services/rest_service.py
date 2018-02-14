from flask import Flask, request
from flask_cors import CORS

import config
import json
from db import dao
from db.entities import SearchParameters, Torrent, Metric

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/torrents/search')
def search():
    name = request.args.get('name', None)
    category = request.args.get('category', None)
    order = request.args.get('order', None)
    skip = request.args.get('skip', '')
    limit = request.args.get('limit', '')
    search_parameters = SearchParameters(name, category, order, skip if skip.isdigit() else None,
                                         limit if limit.isdigit() else None)
    results = dao.search(search_parameters)
    return json.dumps(results, cls=TorrentsListJSONEncoder)


def results_to_json(results):
    return json.dumps(results)


def start_api():
    app.config.update(
        DEBUG=config.rest_api_debug,
        APPLICATION_ROOT='torrents'
    )
    app.run()


class TorrentsListJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Torrent) or isinstance(o, Metric):
            dictionary = {}
            for attr in o.__dict__:
                dictionary[attr] = o.__getattribute__(attr)
            return dictionary
        else:
            raise TypeError

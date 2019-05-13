# -*- coding: utf-8 -*-

from flask import Flask
from flask import Blueprint
import flask_restful as restful
from v2.api.NSSelectionInterface import NSSelection

routes = [
    dict(resource=NSSelection, urls=['/NSSelection'], endpoint='NSSelectionInterface')
]

def create_app():
    app = Flask(__name__, static_folder='static')
    bp = Blueprint('v2',__name__,static_folder='static')
    api = restful.Api(bp,catch_all_404s=True)
    for route in routes:
        api.add_resource(route.pop('resource'), *route.pop('urls'), **route)
    app.register_blueprint(bp,url_prefix='/nnssf-nsselection/v2')
    return app

if __name__ == '__main__':
    print("Creating NSSF")
    create_app().run(host='127.0.0.1',port=5011,debug=True)
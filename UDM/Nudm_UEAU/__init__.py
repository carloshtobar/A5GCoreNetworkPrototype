# -*- coding: utf-8 -*-

from flask import Flask
from flask import Blueprint
import flask_restful as restful
from v1.api.AuthDataGeneration import AuthDataGeneration

routes = [
    dict(resource=AuthDataGeneration, urls=['/AuthDataGeneration'], endpoint='AuthDataGeneration')
]

def create_app():
    app = Flask(__name__, static_folder='static')
    bp = Blueprint('v1',__name__,static_folder='static')
    api = restful.Api(bp,catch_all_404s=True)
    for route in routes:
        api.add_resource(route.pop('resource'), *route.pop('urls'), **route)
    app.register_blueprint(bp,url_prefix='/nudm-ueau/v1')
    return app

if __name__ == '__main__':
    print("Creating UDM")
    create_app().run(host='127.0.0.1',port=5031,debug=True)
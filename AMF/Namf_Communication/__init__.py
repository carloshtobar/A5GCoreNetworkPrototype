# -*- coding: utf-8 -*-

from flask import Flask
from flask import Blueprint
import flask_restful as restful
from v1.api.eNBAndAMFInterface import InterfaceeNBSide
import sys

routes = [
    dict(resource=InterfaceeNBSide, urls=['/amfeNBInterface'], endpoint='eNBAndAMFInterface')
]

def create_app():
    app = Flask(__name__, static_folder='static')
    bp = Blueprint('v1',__name__,static_folder='static')
    api = restful.Api(bp,catch_all_404s=True)
    for route in routes:
        api.add_resource(route.pop('resource'), *route.pop('urls'), **route)
    app.register_blueprint(bp,url_prefix='/namf-comm/v1')
    return app

num_amf_instance = int(sys.argv[1])
if __name__ == '__main__':
    print("Creating AMF ",num_amf_instance)
    create_app().run(host='127.0.0.1',port=5000+num_amf_instance,debug=True)
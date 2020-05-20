from flask import Flask, jsonify
from flask_cors import CORS
from models import setup_db, Plant


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'content-type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET', 'POST', 'PATCH', 'DELETE', 'OPTIONS')
        return response

    @app.route('/')
    def hello():
        return jsonify({'message': 'Hello, World!'})

    @app.route('/smiley')
    def smiley():
        return ':-)'

    return app

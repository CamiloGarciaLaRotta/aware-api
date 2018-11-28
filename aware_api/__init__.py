from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import logging
import os

def create_app(cfg=None):
    app = Flask(__name__)
    load_config(app, cfg)
    CORS(app)
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.INFO)

    # from models import ...

    @app.route('/api/register', methods=['GET'])
    def register():
        '''
        Return a new ID that will subsequently used to store awareness information in the DB
        '''
        logger.info('GET')
        return jsonify({'status': 'ok'}), 200

    @app.route('/api/process', methods=['POST'])
    def routes_get():
        '''
        Process the face image receied in the payload and return awareness characteristics
        '''
        if not request.data:
            missing_payload_message = 'malformed POST request: missing payload'
            logger.warn(missing_payload_message)
            error = {'status' : 'error', 'error': missing_payload_message}
            res =  jsonify(error), 400
            return res

        return jsonify({'status': 'ok'}), 200

    return app

def load_config(app, cfg):
    # Load a default configuration file
    app.config.from_pyfile('config/default.cfg')

    # If cfg is empty try to load config file from environment variable
    if cfg is None and 'AWARE_CFG' in os.environ:
        cfg = os.environ['AWARE_CFG']

    if cfg is not None:
        app.config.from_pyfile(cfg)

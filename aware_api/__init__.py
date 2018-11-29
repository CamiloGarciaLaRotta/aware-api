from flask import Flask, jsonify, request, Response
from flask_cors import CORS

from pydocumentdb import document_client

import logging
import uuid
import json
import os


def create_app(cfg=None):
    app = Flask(__name__)
    load_config(app, cfg)
    CORS(app)
    logger = logging.getLogger('waitress')
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # setup DB handler
    client = document_client.DocumentClient(app.config['DB_URI'], {'masterKey': app.config['DB_KEY']})
    # Read databases and take first since id should not be duplicated.
    db = next((data for data in client.ReadDatabases() if data['id'] == app.config['DB_NAME']))
    # Read collections and take first since id should not be duplicated.
    coll = next((coll for coll in client.ReadCollections(db['_self']) if coll['id'] == app.config['COLL_NAME']))

    @app.route('/api/register', methods=['GET'])
    def register():
        '''Register a new user to the Aware service

        Returns:
            dict: a JSON response with the the new user's unique id
        '''
        logger.info('GET /api/register')
        return jsonify({'status': 'ok', 'id':register_user(coll, client)}), 200

    @app.route('/api/process', methods=['POST'])
    def routes_get():
        '''
        Process the face image receied in the payload and return awareness characteristics
        Payload: {"id":<user_id>, "image":<base64>}
        '''
        if not request.data:
            missing_payload_message = 'malformed POST request: missing payload'
            logger.warn(missing_payload_message)
            error = {'status' : 'error', 'error': missing_payload_message}
            return jsonify(error), 400

        payload = json.loads(request.data)

        if 'id' not in payload:
            missing_id_message = 'malformed POST request: missing id'
            logger.warn(missing_id_message)
            error = {'status' : 'error', 'error': missing_id_message}
            return jsonify(error), 400
        if 'image' not in payload:
            missing_image_message = 'malformed POST request: missing image'
            logger.warn(missing_image_message)
            error = {'status' : 'error', 'error': missing_image_message}
            return jsonify(error), 400

        id = payload['id']
        image = payload['image']

        return jsonify({'status': 'ok', 'id': id, 'image': image}), 200

    return app

def load_config(app, cfg):
    # Load a default configuration file
    app.config.from_pyfile('config/default.py')

    # If cfg is empty try to load config file from environment variable
    if cfg is None and 'AWARE_CFG' in os.environ:
        cfg = os.environ['AWARE_CFG']

    if cfg is not None:
        app.config.from_pyfile(cfg)


def register_user(coll: dict, client: document_client.DocumentClient) -> str:
    '''Create a unique id for the new user

    Args:
        coll (dict): collection handler
        client (DocumentClient): DB connection handler

    Returns:
        str: the unique id of the new user
    '''

    while True:
        id = str(uuid.uuid4())
        query = {'query': f'SELECT VALUE COUNT(\'id\') FROM r WHERE r.id = \'{id}\'' }
        result = list(client.QueryDocuments(coll['_self'], query))
        if result[0] == 0:
            client.CreateDocument(coll['_self'], {'id':id, 'transactions': []})
            return id

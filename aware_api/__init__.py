from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import logging
import json
import os
import requests
import uuid
from .DbClient import DbClient
from .SleepyRecognizer import SleepyRecognizer


def create_app(cfg=None):
    app = Flask(__name__)
    load_config(app, cfg)
    CORS(app)
    logger = logging.getLogger('waitress')
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # create a database client
    client = DbClient(app.config)

    # download assets
    download_assets(app.config)

    # load services
    sleepyRecognizer = SleepyRecognizer()

    # from models import ...
    @app.route('/api/register', methods=['GET'])
    def register():
        '''
        Return a new ID that will subsequently used to store awareness information in the DB
        '''
        logger.info('GET /api/register')
        userID = uuid.uuid4()
        client.CreateItem({'id': str(userID)})
        return jsonify({'status': 'ok', 'id':userID}), 200

    @app.route('/api/process', methods=['POST'])
    def routes_get():
        '''
        Process the face image receied in the payload and return awareness characteristics
        Payload: {"id":<user_id>, "image":<base64>}
        '''
        if not request.json:
            missing_payload_message = 'malformed POST request: missing payload'
            logger.warn(missing_payload_message)
            error = {'status' : 'error', 'error': missing_payload_message}
            return jsonify(error), 400

        payload =request.json
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


        userID = str(payload['id'])
        image = str(payload['image'])

        logger.info(userID)
        logger.info(image[:10])

        # logger.info(f'POST /api/process {id}')

        # fetch client record and init results
        dbEntry = client.GetItemById(userID)

        if(dbEntry == None):
            missing_client_record_message = 'client with id ' + userID + ' does not exists'
            return jsonify({'status': 'error', 'error': missing_client_record_message}), 400
        if('Transactions'  not in dbEntry):
            dbEntry['Transactions'] = []


        sleepy_percentage = sleepyRecognizer.recognize(image)
        # process image
        results = {}
        if(sleepy_percentage == -1):
            missing_face_message = 'Picture contained no face'
            return jsonify({'status': 'error', 'error': missing_face_message}), 400

        results['Sleepy'] = sleepy_percentage

        # save results
        dbEntry['Transactions'].append(results)
        client.UpsertItem(dbEntry)


        return jsonify(results), 200

    return app

def load_config(app, cfg):
    # Load a default configuration file
    app.config.from_pyfile('config/default.cfg')

    # If cfg is empty try to load config file from environment variable
    if cfg is None and 'AWARE_CFG' in os.environ:
        cfg = os.environ['AWARE_CFG']

    if cfg is not None:
        app.config.from_pyfile(cfg)

def download_assets(config):
    try:
        os.mkdir('Assets')
    except:
        pass

    assets = config['ASSETS']
    for url in assets.split(','):
        name =  url.split('/')[-1]
        path = 'Assets/' + name
        if os.path.exists(path):
            continue

        print('Downloading ',  name, '...')
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
        print('Finished Downloading: ',  name)


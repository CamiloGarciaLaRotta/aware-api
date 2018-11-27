from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import json

app = Flask(__name__)
app.config.from_object('config')
CORS(app)

@app.route('/api/register', methods=['GET'])
def register():
	'''
	Return a new ID that will subsequently used to store awareness information in the DB
	'''
	# TODO
	return jsonify({'status': 'ok'}), 200

@app.route('/api/process', methods=['POST'])
def routes_get():
	'''
	Process the face image receied in the payload and return awareness characteristics
	'''
	if not request.data:
		missing_payload_message = 'malformed POST request: missing payload'
		app.logger.warn(missing_payload_message)
		error = {'status' : 'error', 'error': missing_payload_message}
		res =  jsonify(error), 400
		return res
	# TODO
	return jsonify({'status': 'ok'}), 200

if __name__ == "__main__":
	app.run()

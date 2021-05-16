import sys
import os
# import io
import json
from typing import Dict

# Type hints
from werkzeug.datastructures import FileStorage
from numpy import array
from typing import Dict

from flask import Flask, Response, jsonify, request
from flask_cors import CORS, cross_origin
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

from utils import setup_logger, allowed_file, file2image, image2b64
from models import detect_apparel, fetch_apparel, CLASSES


logger = setup_logger(__name__)
logger.info('Finished Importing')

# attach logger to system exceptions - https://stackoverflow.com/a/6234491
sys.excepthook = lambda exc_type, val, traceback: logger.error('Unhandled exception:', exc_info=val)

app = Flask(__name__)
cors = CORS(app=app)
app.config['CORS_HEADER'] = 'Content-Type'

if 'PRODUCTION' not in os.environ:
    logger.info('Models should be in models folder in local run')
    app.config['DEBUG'] = True


@app.route('/')
@cross_origin()
def home():
    return jsonify({'message': 'You\'ve reached the Fashion Search EndPoint'}), 200


@app.route('/inference', methods=['POST'])
@cross_origin()
def inference():
    if 'file' not in request.files:
        return Response({'error': 'No file part'}, status=412)

    file: FileStorage = request.files['file']

    if file.filename == '':
        return Response({'error': 'No file selected'}, status=417)

    if allowed_file(file.filename):
        image = file2image(file)
        predictions: array = detect_apparel(image)
        apparels = fetch_apparel(image, predictions) # sent return key value pairs of apparels found
        # output = { CLASSES[idx] : image2b64(apparel) for idx, apparel in enumerate(apparels)}
        return jsonify(apparels), 200

    else:
        return Response({'error': f'{file.mimetype} not allowed'}, status=412)

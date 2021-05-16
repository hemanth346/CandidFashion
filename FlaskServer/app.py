import sys
import os
# import io
import json

# Type hints
from werkzeug.datastructures import FileStorage
from numpy import array

from flask import Flask, request, render_template, redirect, url_for, flash, Response, jsonify
from flask_cors import CORS, cross_origin
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

from utils import setup_logger, allowed_file, file2image, image2b64
from models import detect_apparel, fetch_apparel, CLASSES


logger = setup_logger(__name__)

# attach logger to system exceptions - https://stackoverflow.com/a/6234491
sys.excepthook = lambda exc_type, val, traceback: logger.error('Unhandled exception:', exc_info=val)

app = Flask(__name__)
cors = CORS(app=app)
app.config['CORS_HEADER'] = 'Content-Type'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # limit file size to 10mb
app.secret_key = 'super secret key'
app_root = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
@cross_origin()
def home():
    return render_template('home.html', current_page='home')


@app.route('/inference', methods=['GET', 'POST'])
@cross_origin()
def inference():
    if request.method == 'GET':
        return render_template('inference.html', current_page='inference')

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
    ### !! Not sure how to add render and display separate cards/containers for each apparel
        return jsonify(apparels), 200

    else:
        return Response({'error': f'{file.mimetype} not allowed'}, status=412)


@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(413)
def request_entity_too_large(error):
    flash('The file is too large. The maximum allowed size is 10 MB.')
    return redirect(url_for(inference))


if __name__ == '__main__':
    app.run(debug=True)  # developer mode

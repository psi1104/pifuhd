import io
import os
import sys
import shutil
import uuid
import copy

import threading
import time
from queue import Empty, Queue

from lightweight_human_pose_estimation_pytorch.get_pose import get_pose, get_pose_model
from apps.simple_test import run, get_render_model

from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from Naked.toolshed.shell import execute_js

DATA_FOLDER = 'img_data'
CONVERTER_PATH = './static/converter.js'

pose_model = get_pose_model()
render_model = get_render_model()

app = Flask(__name__, template_folder='static')

@app.route('/predict', methods=['POST'])
def predict():
    input_file = request.files['source']

    if input_file.content_type not in ['image/jpeg', 'image/jpg', 'image/png']:
        return jsonify({'message': 'Only support jpeg, jpg or png'}), 400

    f_id = str(uuid.uuid4())
    fname = secure_filename(input_file.filename)

    # save image to upload folder
    os.makedirs(os.path.join(DATA_FOLDER, f_id), exist_ok=True)
    input_file.save(os.path.join(DATA_FOLDER, f_id, fname))

    image_path = os.path.join(DATA_FOLDER, f_id, fname)

    get_pose(pose_model, image_path)

    data_path = os.path.join(DATA_FOLDER, f_id)

    run(render_model, data_path)

    # result = muterun_js(CONVERTER_PATH, data_path)
    # print(type(result.stdout))
    # result = json.dumps(result.stdout)
    # print(type(resultß))

    execute_js(CONVERTER_PATH, data_path)

    result = os.path.join(data_path, 'model.gltf')

    return send_file(result, mimetype='gltf/json')

@app.route('/health')
def health():
    return "ok"

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port='80')




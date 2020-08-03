import os
import sys
import shutil
import uuid

import threading
import time
from queue import Empty, Queue

from lightweight_human_pose_estimation_pytorch.get_pose import get_pose, get_pose_model
from apps.simple_test import render_obj, get_render_model
from apps.clean_mesh import meshcleaning

from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from Naked.toolshed.shell import execute_js

DATA_FOLDER = 'img_data'
CONVERTER_PATH = './static/converter.js'

pose_model = get_pose_model()
render_model = get_render_model()

requests_queue = Queue()

#remove image data
def remove_image(f_id):
    data_path = os.path.join(DATA_FOLDER, f_id)
    shutil.rmtree(data_path)

app = Flask(__name__, template_folder='static')

BATCH_SIZE=1
CHECK_INTERVAL=0.1

def run(input_file, f_id):

    fname = secure_filename(input_file.filename)

    # save image to upload folder
    os.makedirs(os.path.join(DATA_FOLDER, f_id), exist_ok=True)
    input_file.save(os.path.join(DATA_FOLDER, f_id, fname))

    image_path = os.path.join(DATA_FOLDER, f_id, fname)

    get_pose(pose_model, image_path)

    data_path = os.path.join(DATA_FOLDER, f_id)

    render_obj(render_model, data_path)

    meshcleaning(data_path)

    execute_js(CONVERTER_PATH, data_path)

    result_path = os.path.join(data_path, 'model.glb')

    return result_path

def handle_requests_by_batch():
    try:
        while True:
            requests_batch = []

            while not (
              len(requests_batch) >= BATCH_SIZE # or
              #(len(requests_batch) > 0 #and time.time() - requests_batch[0]['time'] > BATCH_TIMEOUT)
            ):
              try:
                requests_batch.append(requests_queue.get(timeout=CHECK_INTERVAL))
              except Empty:
                continue

            batch_outputs = []

            for request in requests_batch:
                batch_outputs.append(run(request['input'][0], request['input'][1]))

            for request, output in zip(requests_batch, batch_outputs):
                request['output'] = output

    except Exception as e:
        while not requests_queue.empty():
            requests_queue.get()
        print(e)

threading.Thread(target=handle_requests_by_batch).start()

@app.route('/predict', methods=['POST'])
def predict():
    print(requests_queue.qsize())
    if requests_queue.qsize() >= 1:
        return jsonify({'message': 'Too Many Requests'}), 429

    input_file = request.files['source']
    f_id = str(uuid.uuid4())

    if input_file.content_type not in ['image/jpeg', 'image/jpg', 'image/png']:
        return jsonify({'message': 'Only support jpeg, jpg or png'}), 400

    req = {
        'input': [input_file, f_id]
    }

    requests_queue.put(req)

    while 'output' not in req:
        time.sleep(CHECK_INTERVAL)

    result_path = req['output']

    result = send_file(result_path, mimetype='model/gltf-binary')

    remove_image(f_id)

    return result

@app.route('/health')
def health():
    return "ok"

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port='80')




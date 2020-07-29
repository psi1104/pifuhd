import os
from lightweight_human_pose_estimation_pytorch.get_pose import get_pose
from apps.simple_test import run

from flask import Flask, render_template, send_file
from Naked.toolshed.shell import execute_js, muterun_js

app = Flask(__name__, template_folder='static')

@app.route('/predict')
def predict():

    image_path = 'sample_images/irene_body.jpg'  # example image

    # output pathes

    get_pose(image_path)

    run()

    success = execute_js('./static/app.js')

    return send_file(result, mimetype='model/gltf+json')

@app.route('/health')
def health():
    return "ok"

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port='8104')




from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import base64
from io import BytesIO
from model import predict, predict_image  # Import the prediction function from model.py
import os
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import io

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')  

# Route for handling image upload via form submission
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Secure the filename and save the image
        filename = secure_filename(file.filename)
        img = Image.open(file)
        
        # Predict using the model
        label, confidence = predict_image(img)
        
        return jsonify({
            'result': label,
            'confidence': f'{confidence * 100:.2f}%',
        })
    
    return jsonify({'error': 'Invalid file format'}), 400


@app.route('/process-frame', methods=['POST'])
def process_frame():
    try:
        data = request.json
        image_data = data['image']
        img_data = base64.b64decode(image_data.split(",")[1])
        label, confidence = predict(img_data)
        
        return jsonify({"result": label, "confidence": confidence})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def handle_image(data):

    try:
        img_data = data['image']
        
        if img_data.startswith("data:image"):
            img_data = img_data.split(",")[1] 
        
        img_data = base64.b64decode(img_data)

        print(f"Received image data: {img_data[:100]}...")  

        label, confidence = predict(img_data)

        emit('result', {'result': label, 'confidence': confidence})
    except Exception as e:

        print(f"Error processing image: {e}")
        emit('error', {'error': str(e)})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)

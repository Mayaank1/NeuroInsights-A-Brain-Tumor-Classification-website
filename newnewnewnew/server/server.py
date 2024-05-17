from flask import Flask, request, jsonify, session
from pymongo import MongoClient
from flask_cors import CORS

import os
import numpy as np

from gridfs import GridFS
import bcrypt
from flask_session import Session
import tensorflow as tf
import pickle
import cv2
import cv2
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from joblib import Parallel, delayed
import joblib
from tensorflow.keras.models import load_model

# Get the absolute path to the saved model file
# model_file_path = os.path.abspath('model.sav')
# app instance

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)


# Flask route to check session status


@app.route('/api/submit_register_form', methods=['POST'])
def submit_register_form():
    try:
        name = request.form['name']
        email = request.form['email']
        # phone = request.form['phone']
        # name = request.form['name']
        password = request.form['password']

        # image_file = request.files['image']
        # if image_file:
        #     # Save the image to GridFS and get the file ID
        #     file_id = fs.put(image_file.stream, filename=image_file.filename)

        # Store other data and the image file ID in MongoDB
        # Hash the password
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())

# Store other data and the hashed password in MongoDB
        model_data = {
            'name': name,
            'email': email,
            # 'phone': phone,
            # 'name': name,
            # Store the hashed password as a string
            'password': hashed_password.decode('utf-8')
        }


    except Exception as e:
        return jsonify({'error': e}), 500



@app.route('/api/submit_login_form', methods=['POST'])
def submit_login_form():
    try:

        name = request.form['name']
        entered_password = request.form['password']

        stored_hashed_password = db.models.find_one(
            {'name': name})['password']
        if bcrypt.checkpw(entered_password.encode('utf-8'), stored_hashed_password.encode('utf-8')):

            session['authenticated'] = True
            session['name'] = name

            response_data = {
                'message': session['name'],
            }

            return jsonify(response_data), 200

        else:
            # Invalid credentials
            response_data = {
                'error': 'Invalid credentials',
            }
            return jsonify(response_data), 401

        # Example: You can send a response back to the client with the model ID

    except Exception as e:
        return jsonify({'error': e}), 500


@app.route('/api/predict', methods=['POST'])
@app.route('/api/predict', methods=['POST'])
def predict():

    # if session.get('authenticated'):
    #     return jsonify({'message': 'Session is active'}), 200

    requested_image = request.files['image']

    image_path = 'uploads/' + requested_image.filename
    requested_image.save(image_path)

    try:
        img = tf.io.read_file(image_path)

        # img = cv2.imread(image_path)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # model1 = tf.keras.models.load_model('terrain_nonterrain.h5')
        # resize = tf.image.resize(img, (256, 256))
        # # resize.numpy().astype(int)
        # yhat = model1.predict(np.expand_dims(resize/255, 0))

  
  # Compile image
        img = tf.image.decode_image(img)

  # Resize image
        img = tf.image.resize(img, [256,256])

  # Scale the tensor
        img = img / 255
        class_names = ['glioma','meningioma' ,'notumor', 'pituitary']
        class_names=np.array(class_names)
        print(type(class_names))
        image = img[:,:,:3]
        model = joblib.load("model.sav")

        pred = model.predict(np.expand_dims(image, axis=0))
        # plt.title(class_names[pred[0].argmax()])
        print(class_names[pred[0].argmax()])
        pre=class_names[pred[0].argmax()]
        return jsonify(pre)

        

    except Exception as e:
                return jsonify({'error': str(e)})

        # if os.path.exists(image_path):
        #     os.remove(image_path)



if __name__ == "__main__":
    app.run(debug=True, port=8080)


# def predict():
#     try:

#         age = 30
#         salary = 87000
#         load_model = pickle.load(open(model_file_path, 'rb'))

#         # Make a prediction using the loaded model
#         prediction = load_model.predict(([[30, 87000]]))

#         # You can convert the prediction to a human-readable label if needed
#         # For example, if your labels are 0 and 1, you can map them to 'No' and 'Yes'
#         prediction_label = 'Yes' if prediction[0] == 1 else 'No'
#         print(prediction_label)

#         result = {
#             'prediction': prediction_label
#         }
#         return jsonify(result)

#     except Exception as e:
#         return jsonify({'error': str(e)})

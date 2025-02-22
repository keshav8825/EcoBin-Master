import os
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import load_img
import numpy as np


app = Flask(__name__)
model = load_model('resnet.h5')
target_img = os.path.join(os.getcwd(), '\static\images')
@app.route('/')
def index_view():
    return render_template('index.html')
ALLOWED_EXT = set(['jpg', 'jpeg', 'png'])
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXT
        
#Function to load and prepare the image in right shape
def read_image(filename):
    img = load_img(filename, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(img, axis=0)
    return x
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join('static/images', filename)
            file.save(file_path)
            img = read_image(file_path) #preprocessing image
            class_prediction = model.predict(img)
            classes_x = np.argmax(class_prediction, axis = 1)
            if classes_x == 1:
                waste = "Recyclable"
            else:
                waste = "Organic"
            return render_template('predict.html', waste= waste, prob = class_prediction, user_image= file_path)
        else:
            return "Unable to read the file. Please check file extension"
        
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=8000)

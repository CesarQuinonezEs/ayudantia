from flask import Flask, request, render_template, redirect, url_for
from keras.models import load_model
from keras.applications.resnet_v2 import preprocess_input,decode_predictions
from keras.preprocessing import image
import numpy as np
import os
import cv2
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Cargar el modelo
model_path = "models/CIDBIS.h5"
model = load_model(model_path)


def preprocess_image(img_path):
    
    img = cv2.imread(img_path)
    
    # Resize the image to the required dimensions (224x224)
    img_resized = cv2.resize(img, (224, 224))
    
    # Convert the image to float32 and normalize to the range [0, 1]
    img_normalized = img_resized.astype(np.float32) / 255.0
    
    # Expand dimensions to add the batch size (1, 224, 224, 3)
    img_batch = np.expand_dims(img_normalized, axis=0)
    
    # Use preprocess_input from keras.applications to further preprocess the image for ResNet50V2
    img_preprocessed = preprocess_input(img_batch)
    return img_preprocessed

def model_predict(img_path, model):
    img = preprocess_image(img_path)

    preds = model.predict(img)
    return preds

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            prediction = model_predict(filepath,model)
            pred_class =    decode_predictions(prediction, top=1)
            pred_class2 = decode_predictions(prediction,top=3)
            
            for i, (imagenet_id, label, score) in enumerate(pred_class2[0]):
                print(f"{i+1}: {label} ({score * 100:.2f}%)")
            result = str(pred_class[0][0][1]) 
            print(result)
            
            return render_template('result.html', prediction=result)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
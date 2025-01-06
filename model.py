import base64
from PIL import Image
import io
from tensorflow import keras
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array


model = keras.models.load_model('./2024-10-20_first_model_vgg16.keras')


actions = [
    'normal driving', 'texting - right', 'phone - right', 'texting - left',
    'phone - left', 'radio', 'drinking', 'behind', 'hair and makeup', 'passenger'
]

def predict_image(image):
    # Preprocess the image
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0  # Normalize the image
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    
    # Make prediction
    predictions = model.predict(img_array)
    pred_class = np.argmax(predictions, axis=1)
    confidence = np.max(predictions)
    
    if confidence * 100 > 60:
        return actions[pred_class[0]], confidence
    return "Uncertain", confidence

def predict(image_bytes):
    print(image_bytes)
    try:
        if isinstance(image_bytes, str):
            if image_bytes.startswith('data:image'):
                image_bytes = image_bytes.split(",")[1] 

        img_data = base64.b64decode(image_bytes)

        img = Image.open(io.BytesIO(img_data))

        img = img.resize((224, 224))

        img_array = img_to_array(img) / 255.0  
        img_array = np.expand_dims(img_array, axis=0)  
        
        predictions = model.predict(img_array)
        
        pred_class = np.argmax(predictions, axis=1)
        confidence = np.max(predictions)
        
        if confidence * 100 > 60:
            return actions[pred_class[0]], confidence
        else:
            return "Uncertain", confidence
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return "Error", 0.0
import base64
import json
import pickle
import os
from wavelet import w2d
import cv2
import numpy as np

__model = None
__class_name_to_number__ = {}
__number_to_class_name__ = {}
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _find_artifact(name, fallback_name):
    """Find artifact file with fallback support."""
    primary = os.path.join(_BASE_DIR, "artifacts", name)
    fallback = os.path.join(_BASE_DIR, "artifacts", fallback_name)
    
    if os.path.exists(primary):
        return primary
    if os.path.exists(fallback):
        return fallback
    raise FileNotFoundError(f"Could not find {name} or {fallback_name}")


def classify_image(image_base64, file_path=None):
    """Classify faces in the provided image."""
    if not __model:
        raise RuntimeError("Model not loaded. Call load_saved_artifacts() first.")
    
    cropped_faces = croptofrontface(file_path, image_base64)
    result = []
    
    for face in cropped_faces:
        try:
            scaled_raw_img = cv2.resize(face, (32, 32))
            scaled_gray = cv2.cvtColor(scaled_raw_img, cv2.COLOR_BGR2GRAY)
            face_wavelet = w2d(scaled_gray, 'db1', 5)
            combined_img = np.vstack((scaled_raw_img.reshape(32*32*3, 1), face_wavelet.reshape(32*32, 1)))
            combined_img = combined_img.reshape(1, 32*32*3 + 32*32).astype(float)
            
            prediction = __model.predict(combined_img.reshape(1, -1))[0]
            
            # Try to get probability if available, otherwise use default 1.0
            if hasattr(__model, 'predict_proba'):
                probability = float(np.round(__model.predict_proba(combined_img.reshape(1, -1)).max(), 2))
            else:
                probability = 1.0
            
            result.append({
                "class": __number_to_class_name__.get(int(prediction), "Unknown"),
                "class_probability": probability,
                "class_dictionary": __class_name_to_number__
            })
        except Exception as e:
            print(f"Error processing face: {e}")
            continue
    
    return result


def load_saved_artifacts():
    """Load model and class labels from disk."""
    global __model, __class_name_to_number__, __number_to_class_name__
    
    print("Loading saved artifacts...")
    
    class_dict_path = _find_artifact("class_dictionary.json", "sports_person_classifier_labels.json")
    model_path = _find_artifact("saved_model.pkl", "sports_person_classifier.pkl")
    
    with open(class_dict_path, "r") as f:
        __class_name_to_number__ = json.load(f)
        __number_to_class_name__ = {v: k for k, v in __class_name_to_number__.items()}
    
    with open(model_path, "rb") as f:
        __model = pickle.load(f)
    
    print("Artifacts loaded successfully.")


def croptofrontface(img_path, image_base64_data):
    """Extract face regions with eyes from image."""
    face_cascade_path = os.path.join(_BASE_DIR, "haarcascades", "haarcascade_frontalface_default.xml")
    eye_cascade_path = os.path.join(_BASE_DIR, "haarcascades", "haarcascade_eye.xml")
    
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
    
    if img_path:
        img = cv2.imread(img_path)
    else:
        try:
            img_data = base64.b64decode(image_base64_data)
            img_array = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        except Exception as e:
            print(f"Error decoding image: {e}")
            return []
    
    if img is None:
        return []
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    cropped_faces = []
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            cropped_faces.append(roi_color)
    
    return cropped_faces


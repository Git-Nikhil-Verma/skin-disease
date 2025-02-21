from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
import os
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

# Load TensorFlow Lite model
MODEL_PATH = "skin_cancer_cnn.tflite"

if not os.path.exists(MODEL_PATH):
    print("❌ Model file not found! Ensure it's available.")
else:
    print("✅ TFLite Model Found!")

# Load TFLite interpreter
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

# Get input and output tensor details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Function to preprocess and predict
def predict_skin_cancer(img_path):
    try:
        print(f"🔍 Processing Image: {img_path}")

        # Load and preprocess image
        img = Image.open(img_path).resize((224, 224))  # Resize to match model input
        img_array = np.array(img) / 255.0  # Normalize
        img_array = np.expand_dims(img_array, axis=0).astype(np.float32)  # Expand dimensions

        print("🧠 Making Prediction...")
        interpreter.set_tensor(input_details[0]["index"], img_array)
        interpreter.invoke()

        prediction = interpreter.get_tensor(output_details[0]["index"])[0]
        print(f"🔎 Raw Prediction Output: {prediction}")

        class_label = "Malignant" if prediction > 0.5 else "Benign"
        return class_label
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        return "Error predicting image."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Predict the class
    class_label = predict_skin_cancer(file_path)
    return jsonify({"prediction": class_label, "image": file_path})

if __name__ == "__main__":
    app.run(debug=True)

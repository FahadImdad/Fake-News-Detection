
from flask import Flask, request, jsonify
import pickle
from pathlib import Path
import re
import string

app = Flask(__name__)

# --- Preprocessing Function (same as training) ---
def preprocess(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text)
    text = re.sub(r'\@\w+|\#','', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# --- Load Models & Vectorizer ---
base_path = Path(__file__).resolve().parent
model_path = base_path / "model" / "all_models.pkl"
vectorizer_path = base_path / "model" / "vectorizer.pkl"

if not model_path.exists() or not vectorizer_path.exists():
    raise FileNotFoundError("Model or vectorizer file not found. Please ensure both exist in the 'model' folder.")

with open(model_path, "rb") as f:
    all_models = pickle.load(f)

with open(vectorizer_path, "rb") as f:
    vectorizer = pickle.load(f)

# --- Routes ---
@app.route("/")
def home():
    return "✅ Fake News Detection Flask API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Please provide 'title' and 'content' in JSON body"}), 400

    # Preprocess
    full_text = f"{data['title']} {data['content']}"
    cleaned_text = preprocess(full_text)
    vect_text = vectorizer.transform([cleaned_text])

    # Predictions
    predictions = {}
    for model_name, model in all_models.items():
        try:
            pred = int(model.predict(vect_text)[0])
            predictions[model_name] = pred
        except Exception as e:
            predictions[model_name] = f"Error: {str(e)}"

    return jsonify({
        "title": data["title"],
        "predictions": predictions
    })

if __name__ == "__main__":
    app.run(debug=True)





































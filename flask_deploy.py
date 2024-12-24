from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import joblib
import pandas as pd

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Load the saved Random Forest model
try:
    rf_model = joblib.load('wine_quality_model.pkl')
except Exception as e:
    rf_model = None
    print(f"Model loading failed: {e}")

# Define the list of features (ensure this matches the training data)
significant_features = ['fixed acidity', 'volatile acidity', 'citric acid',
                        'chlorides', 'free sulfur dioxide', 'total sulfur dioxide',
                        'density', 'pH', 'sulphates', 'alcohol']

@app.route('/predict', methods=['POST'])
def predict():
    if rf_model is None:
        return jsonify({'error': 'Model not loaded properly'}), 500
    
    # Get the JSON data from the request
    data = request.get_json()
    
    # Validate the input data
    if not isinstance(data, list):
        return jsonify({'error': 'Invalid input format. Expected a list of dictionaries.'}), 400
    
    # Convert the JSON data to a DataFrame
    df = pd.DataFrame(data)

    # Ensure the DataFrame has the required columns
    missing_features = [feature for feature in significant_features if feature not in df.columns]
    if missing_features:
        return jsonify({'error': f'Missing features: {", ".join(missing_features)}'}), 400

    # Predict using the Random Forest model
    try:
        predictions = rf_model.predict(df[significant_features])
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {e}'}), 500

    # Map predictions to labels
    predicted_labels = ['good' if pred == 1 else 'bad' for pred in predictions]

    # Return predictions as JSON
    return jsonify({'predictions': predicted_labels})

if __name__ == '__main__':
    app.run(debug=True)
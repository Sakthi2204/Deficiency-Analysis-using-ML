from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)
# Load pre-trained model and TF-IDF vectorizer
model = joblib.load('model.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Mapping of label indices to deficiency names
label_mapping ={
    0: 'Biotin', 
    1: 'Calcium', 
    2: 'Essential Fatty Acids', 
    3: 'Folate', 
    4: 'Iodine', 
    5: 'Iron', 
    6: 'Magnesium', 
    7: 'Potassium', 
    8: 'Protein-energy', 
    9: 'Vitamin A', 
    10: 'Vitamin B2 – riboflavin', 
    11: 'Vitamin B6', 
    12: 'Vitamin C', 
    13: 'Vitamin D', 
    14: 'Vitamins B1, B12, B3', 
    15: 'Zinc'}

# Function to preprocess input symptoms, vectorize them, and predict deficiencies
def predict_deficiency(symptoms):
    symptoms_combined_text = ' '.join(symptoms.split(', '))
    symptoms_tfidf = tfidf_vectorizer.transform([symptoms_combined_text])
    predicted_labels = model.predict_proba(symptoms_tfidf)
    top_three_indices = (-predicted_labels).argsort(axis=1)[:, :3]
    predicted_deficiencies = [[label_mapping[index] for index in row] for row in top_three_indices]
    return predicted_deficiencies

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    symptoms = data.get('symptoms', '')
    predicted_deficiencies = predict_deficiency(symptoms)
    print(predicted_deficiencies)
    return jsonify({'deficiencies': predicted_deficiencies})

if __name__ == "__main__":
    app.run(debug=True)

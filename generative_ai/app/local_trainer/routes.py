from flask import Blueprint, render_template, request, jsonify
import spacy
from spacy.matcher import Matcher

local_trainer = Blueprint('local_trainer', __name__)

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

# Create a matcher and add custom patterns
matcher = Matcher(nlp.vocab)
symptom_patterns = [
    {"label": "SYMPTOM", "pattern": [{"LOWER": "fever"}]},
    {"label": "SYMPTOM", "pattern": [{"LOWER": "cough"}]},
    {"label": "SYMPTOM", "pattern": [{"LOWER": "difficulty"}, {"LOWER": "breathing"}]},
]
for pattern in symptom_patterns:
    matcher.add(pattern["label"], [pattern["pattern"]])

# Diagnosis and Prescription Maps
diagnosis_map = {
    "fever": "Common Cold",
    "cough": "Influenza",
    "difficulty breathing": "COVID-19"
}

prescription_map = {
    "Common Cold": "Rest, drink fluids, and take over-the-counter cold medications.",
    "Influenza": "Antiviral medications like Tamiflu, rest, and fluids.",
    "COVID-19": "Isolate, monitor oxygen levels, and consult a doctor for possible antiviral treatment."
}

@local_trainer.route('/')
def index():
    return render_template('local_trainer/index.html')

@local_trainer.route('/get_diagnosis', methods=['POST'])
def get_diagnosis():
    try:
        data = request.json
        symptoms_text = data.get('symptoms')

        # Process the symptoms text using SpaCy
        doc = nlp(symptoms_text)
        matches = matcher(doc)

        # Extract matched symptoms
        extracted_symptoms = [doc[start:end].text.lower() for match_id, start, end in matches]

        diagnosis = None
        for symptom in extracted_symptoms:
            if symptom in diagnosis_map:
                diagnosis = diagnosis_map[symptom]
                break

        if diagnosis is None:
            diagnosis = "Unknown condition"
            prescription = "Please consult a healthcare professional for an accurate diagnosis."
        else:
            prescription = prescription_map[diagnosis]

        return jsonify({'diagnosis': diagnosis, 'prescription': prescription})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Error processing symptoms. Please try again later.'}), 500

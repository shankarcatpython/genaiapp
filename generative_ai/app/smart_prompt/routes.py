from flask import Blueprint, render_template, request, jsonify
from . import llm  # Adjust this import based on where llm is located

# Define the blueprint for smart_prompt
smart_prompt = Blueprint('smart_prompt', __name__)

@smart_prompt.route('/')
def index():
    return render_template('smart_prompt/index.html')

@smart_prompt.route('/process_context', methods=['POST'])
def process_context():
    print('accessing process_context')
    context = request.form['context']
    summarize_response = llm.askme_questions_summarize(context)
    suggestive_response = llm.askme_questions_suggestion(context)
    return jsonify({'summarize_response': summarize_response, 'suggestive_response': suggestive_response})
    print(context)
from flask import Blueprint, render_template, jsonify, request
import sqlite3
import spacy
import numpy as np
import openai  # Import OpenAI library

import generative_ai.app.config as config

openai.api_key = config.config.OPENAI_API_KEY 

# Define the blueprint for gen_retrieve
gen_retrieve = Blueprint('gen_retrieve', __name__)

# Initialize spaCy
nlp = spacy.load('en_core_web_sm')

def fetch_data_from_db():
    # Connect to the SQLite database
    conn = sqlite3.connect('genieai.db')
    c = conn.cursor()
    c.execute("SELECT chunk, embedding FROM embeddings")
    rows = c.fetchall()
    conn.close()
    
    # Extract chunks and embeddings
    chunks = []
    embedding_vectors = []
    for row in rows:
        chunk = row[0]
        embedding = np.frombuffer(row[1], dtype=np.float32)
        chunks.append(chunk)
        embedding_vectors.append(embedding)
    
    return chunks, embedding_vectors

def calculate_similarity(user_input, chunks, embedding_vectors):
    # Generate embedding for user input
    user_doc = nlp(user_input)
    user_vector = user_doc.vector

    # Calculate cosine similarity between user input and stored embeddings
    similarities = []
    for i in range(len(embedding_vectors)):
        similarity = np.dot(user_vector, embedding_vectors[i]) / (np.linalg.norm(user_vector) * np.linalg.norm(embedding_vectors[i]))
        similarities.append((similarity, chunks[i]))
    
    # Sort by similarity score in descending order
    similarities.sort(key=lambda x: x[0], reverse=True)
    return similarities[:2]  # Return top 2 most similar chunks

@gen_retrieve.route('/')
def index():
    # Render the main HTML page
    return render_template('gen_retrieve/index.html')

@gen_retrieve.route('/process', methods=['POST'])
def process():
    # Get user input from the form
    user_input = request.form['user_input']
    
    # Fetch stored chunks and embeddings from the database
    chunks, embedding_vectors = fetch_data_from_db()
    
    # Calculate similarity and prepare context
    similarities = calculate_similarity(user_input, chunks, embedding_vectors)

    # Prepare the context from the most similar chunks
    context = ''
    for similarity in similarities:
        context += similarity[1].replace('"', '') + '\n'
    
    # Prepare the prompt for OpenAI
    summarize = "Summarize the following passage for a 5-year-old in simple terms:\n\n"
    prompt_to_LLM = summarize + context

    # Call the OpenAI API using the "gpt-3.5-turbo" model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt_to_LLM}
        ],
        max_tokens=150,
        temperature=0.7,
    )

    # Extract the summary from the API response
    summary = response['choices'][0]['message']['content'].strip()

    # Return the results as JSON
    return jsonify({'summary': summary, 'prompt': prompt_to_LLM})

from flask import Blueprint, render_template, jsonify, request
import sqlite3
import openai

import generative_ai.app.config as config

openai.api_key = config.config.OPENAI_API_KEY  # Ensure you set your API key# Ensure you set your API key

# Initialize the blueprint
anomaly_guard = Blueprint('anomaly_guard', __name__)

# Database connection function
def get_db_connection():
    try:
        conn = sqlite3.connect('genieai.db')
        conn.row_factory = sqlite3.Row 
        print("Database connection successful")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

# Route to render the main page
@anomaly_guard.route('/')
def index():
    return render_template('anomaly_guard/index.html')

# API to get table names
@anomaly_guard.route('/api/tables')
def get_tables():
    conn = get_db_connection()
    print("Establishing connection to database")
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        tables = conn.execute('SELECT DISTINCT table_name FROM anomaly').fetchall()
        return jsonify([table[0] for table in tables])
    except sqlite3.Error as e:
        print(f"SQL error: {e}")
        return jsonify({"error": "Failed to retrieve table names"}), 500
    finally:
        conn.close()

# API to get features for a selected table
@anomaly_guard.route('/api/features')
def get_features():
    table_name = request.args.get('table_name')
    print(f"Fetching features for table: {table_name}")  # Debug information
    conn = get_db_connection()
    
    # Include the 'anomalies' column in the query
    features = conn.execute('''
        SELECT table_name, analysis_date, feature_name, mean, median, std_dev, min_value, max_value, anomaly_count, anomalies
        FROM anomaly
        WHERE table_name = ?
    ''', (table_name,)).fetchall()
    
    #print(f"Query returned {len(features)} rows")  # Debug information
    conn.close()

    # Convert each row to a dict and handle bytes
    def convert_row(row):
        def safe_decode(value):
            if isinstance(value, bytes):
                try:
                    return value.decode('utf-8')
                except UnicodeDecodeError:
                    return value.decode('latin1', errors='ignore')
            return value

        return {key: safe_decode(value) for key, value in dict(row).items()}

    result = [convert_row(row) for row in features]
    #print(f"Returning {result}")  # Debug information
    return jsonify(result)

@anomaly_guard.route('/api/generate_summary', methods=['POST'])
def generate_summary():
    try:
        data = request.json
        feature_name = data.get('feature_name')
        mean = data.get('mean')
        median = data.get('median')
        std_dev = data.get('std_dev')
        min_value = data.get('min_value')
        max_value = data.get('max_value')
        anomaly_count = data.get('anomaly_count')

        if not all([feature_name, mean, median, std_dev, min_value, max_value, anomaly_count]):
            raise ValueError("Missing required data in the request payload")

        prompt = (
            f"Generate a detailed and insightful summary based on the following data:\n"
            f"Feature: {feature_name}\n"
            f"Mean: {mean}\n"
            f"Median: {median}\n"
            f"Standard Deviation: {std_dev}\n"
            f"Minimum Value: {min_value}\n"
            f"Maximum Value: {max_value}\n"
            f"Anomaly Count: {anomaly_count}\n"
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7
        )

        generated_summary = response.choices[0].message['content'].strip()
        print("Generated summary:", generated_summary)
        return jsonify({'summary': generated_summary})

    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return jsonify({"error": "Failed to generate summary"}), 500

    except Exception as e:
        print(f"General error occurred: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

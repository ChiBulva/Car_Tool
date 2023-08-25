import scripts.GrayPry_AI as GrayPry_AI

from flask import Flask, render_template, request, jsonify, send_file
from jinja2 import Template
import json
import zipfile
import io

app = Flask(__name__)

@app.route('/')
def diagnostic_form():
    return render_template('diagnostic.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Collect form data
    form_data = request.form.to_dict()

    # Convert form data to JSON
    json_data = json.dumps(form_data, indent=4)
    
    try:
        # Convert the JSON string to a dictionary
        json_data = json.loads(json_data)
        
        # Call the function with the dictionary
        question = GrayPry_AI.create_diagnosis_question(json_data)

    except json.JSONDecodeError:
        print("Invalid JSON data")
    
    formatted_response = GrayPry_AI.get_diagnosis_reasons(question)
    return render_template('issues.html', diagnostic=formatted_response)

if __name__ == '__main__':
    app.run(debug=True)

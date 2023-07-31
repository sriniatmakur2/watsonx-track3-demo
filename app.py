from flask import Flask, render_template, request
from flask import jsonify
import os
import requests
import json
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import IAMTokenManager
from dotenv import load_dotenv

app = Flask(__name__)

def configure():
    load_dotenv()

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/answer/", methods = ['POST', 'GET'])
def answer():
    if (request.method == 'GET'):
        return(f"The URL /answer is accessed directly. Try going to '/question' to submit the question")
    
    if (request.method == 'POST'):
        question = request.form['Question']

    configure()

    # Get API Key
    API_KEY = os.environ['IBM_WATSON_API_KEY']
    iam_token_manager = IAMTokenManager(apikey=API_KEY)
    bearer_token = iam_token_manager.get_token()

    # JSON data for watsonx
    data_for_watsonx = {
    "model_id": "google/flan-ul2",
    "input": "Question:\\n" + question + "\\n\\nAnswer:\\n",
    "parameters": {
        "decoding_method": "greedy",
        "max_new_tokens": 100,
        "min_new_tokens": 0,
        "stop_sequences": [],
        "repetition_penalty": 1
        },
    "project_id": "c3761613-049a-437e-b4e0-ae68f77f97f7"
    }

    json_data_for_watsonx = json.dumps(data_for_watsonx)

    # Headers for watsonx
    headers_for_watsonx = {
        'Content-type': 'application/json', 
        'Accept': 'application/json', 
        'Authorization': 'Bearer ' + bearer_token
        }
    
    # Url for watsonx
    url_for_watsonx = 'https://us-south.ml.cloud.ibm.com/ml/v1-beta/generation/text?version=2023-05-29'

    response_from_watsonx = requests.post(url_for_watsonx, data=json_data_for_watsonx, headers=headers_for_watsonx)

    answer = response_from_watsonx.json().get('results')[0].get('generated_text')

    return render_template("answer.html", question = "Question: " + question, answer = "Response: " + answer)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    port = os.environ.get('FLASK_PORT') or 8080
    port = int(port)

    app.run(port=port,host='0.0.0.0')
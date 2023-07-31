from flask import Flask
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
    configure()

    # Get API Key
    API_KEY = os.environ['IBM_WATSON_API_KEY']
    iam_token_manager = IAMTokenManager(apikey=API_KEY)
    bearer_token = iam_token_manager.get_token()

    # JSON data for watsonx
    data_for_watsonx = {
    "model_id": "google/flan-ul2",
    "input": "Answer the following question using only information from the article. If there is no good answer in the article, say \"I don't know\".\\n\\nArticle: \\n###\\nTomatoes are one of the most popular plants for vegetable gardens. Tip for success: If you select varieties that are resistant to disease and pests, growing tomatoes can be quite easy. For experienced gardeners looking for a challenge, there are endless heirloom and specialty varieties to cultivate. Tomato plants come in a range of sizes. There are varieties that stay very small, less than 12 inches, and grow well in a pot or hanging basket on a balcony or patio. Some grow into bushes that are a few feet high and wide, and can be grown is larger containers. Other varieties grow into huge bushes that are several feet wide and high in a planter or garden bed. Still other varieties grow as long vines, six feet or more, and love to climb trellises. Tomato plants do best in full sun. You need to water tomatoes deeply and often. Using mulch prevents soil-borne disease from splashing up onto the fruit when you water. Pruning suckers and even pinching the tips will encourage the plant to put all its energy into producing fruit.\\n###\\n\\nQuestion:\\nIs growing tomatoes easy?\\n\\nAnswer:\\nYes, if you select varieties that are resistant to disease and pests.\\n\\nQuestion:\\nWhat varieties of tomatoes are there?\\n\\nAnswer:\\nThere are endless heirloom and specialty varieties.\\n\\nQuestion:\\nWhy should you use mulch when growing tomatoes?\\n\\nAnswer:\\n",
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
    
    return jsonify(response_from_watsonx.json())

if __name__ == '__main__':
    port = os.environ.get('FLASK_PORT') or 8080
    port = int(port)

    app.run(port=port,host='0.0.0.0')
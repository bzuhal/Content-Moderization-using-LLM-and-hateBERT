from flask import Flask, request, jsonify, Response, make_response
from flask_restx import Api, Resource, Namespace, fields
from flasgger import Swagger
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Gauge, start_http_server, generate_latest, Summary, CollectorRegistry
import requests
import psutil
import os

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')
# prometheus parameters to check
# number_of_requests = Counter('number_of_requests', 'The number of requests, its a counter so the value can increase or reset to zero.')
memory_usage_metric = Gauge('flask_memory_usage_bytes', 'Flask Memory Usage (bytes)')
method_calls_counter = Counter('flask_method_calls', 'Counts the number of method calls in the Flask app', ['method'])
request_duration = Summary('flask_request_duration_seconds', 'Time spent processing a request')

app = Flask(__name__)
api = Api(app)
#swagger = Swagger(app)

metrics = PrometheusMetrics(app, path=None)
metrics.info('app_info', 'Application info', version='1.0.3')
metrics.init_app(app)

@app.route('/metrics', methods=['GET'])
def get_data():
    memory_usage = psutil.Process(os.getpid()).memory_info().rss
    memory_usage_metric.set(memory_usage)

    """Returns all data as plaintext."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# name space for swagger api urls
ns = api.namespace('api', description='Sentences toxic evaluations using LLM or Hetbert')

@ns.route('/moderate_hb')
@ns.doc(description = 'By Calling this method you will evaluate the text using Hetbert')
class ModerateHBApi(Resource):
    moderate_hb_model = api.model('moderate_hb_model', {
        'text': fields.String(required=True, description='Text you want to evaluate'),
        
    })

    @ns.doc(description='sending a Post Request with text parameter to process it')
    @ns.expect(moderate_hb_model)
    def post(self):
        """
            Send your text data to calculate and return the result
        """
        try:
            # increment method calls count by 1
            method_calls_counter.labels(method='moderate_hb').inc()
            # number_of_requests.inc()
            with request_duration.time():
                # Get the text input from the user
                data = request.get_json()
                text = data['text']

                # Analyze the text using the classify_text function
                result = hate_bt(text)

                # Send the result back to the user
                label = result['label']
                toxicity = "toxic" if label == "LABEL_0" else "not_toxic"
                response_message = f"The text '{text}' is '{toxicity}' with a score of {result['score']}"

                return jsonify({'result': response_message})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 400


# @app.route('/moderate_llm', methods=['POST'])
@ns.route('/moderate_llm')
@ns.doc(description = 'By Calling this method you will evaluate the text using LLM')
class ModerateLLMAPI(Resource):
    moderate_llm_model = api.model('moderate_llm_model', {
        'text': fields.String(required=True, description='Text you want to evaluate'),
    })

    @ns.doc(description='sending a Post Request with text parameter to process it')
    @ns.expect(moderate_llm_model)
    def post(self):
        """
            Send your text data to calculate and return the result
        """
        try:
            method_calls_counter.labels(method='moderate_llm').inc()
            # number_of_requests.inc()
            with request_duration.time():
                # Get the text input from the user
                data = request.get_json()
                text = data['text']

                # Analyze the text using the classify_text function
                result = llm(text)
                
                result_str = "toxic" if result else "not_toxic"
                response_message = f"The text '{text}' is '{result_str}'"

                # Send the result back to the user
                return jsonify({'result': response_message})
        except Exception as e:
            return jsonify({'error': str(e)}), 400


# Define a function for analyzing the text
def hate_bt(text):
    # Specify the local directory path
    model_path = "HateBERT_hateval"

    # Load the tokenizer and model from the local directory
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)

    # Create a text classification pipeline
    pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer)

    # Perform text classification
    result = pipeline(text)[0]

    # Print the result (optional)
    print(result)

    return result


def llm(comment, model="vicuna-33b-v1.3", auth_token="group5_s0b4b"):
    # Replace with the actual API base URL
    base_url = "https://vicuna-api.aieng.fim.uni-passau.de/v1"

    # Construct the full URL for the chat completions endpoint
    endpoint = "/chat/completions"
    url = base_url + endpoint

    # Define the data for the chat completion request
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": f"You are a content moderator for a social media site. Check the user role supplied text for containing text requiring moderation, like if it includes any Toxic,Abusive,Threat,Provocative,Obscene,Hatespeech,Racist,Nationalist,Sexist,Homophobic,ReligiousHate, Radicalism language. If so explain it else print single word"},
            {"role": "user", "content": f"'{comment}'."}
        ]
    }

    # Set the headers, including the required authentication header
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    # Make the API request
    response = requests.post(url, json=data, headers=headers)

    # Process the API response
    if response.status_code == 200:
        response_data = response.json()
        assistant_response = response_data['choices'][0]['message']['content'].lower()

        # Define a list of toxic keywords to check for
        toxic_keywords = ["toxic", "abusive", "threat", "provocative", "obscene", "hatespeech", "racist", "nationalist", "sexist", "homophobic", "religioushate", "radicalism"]

        # Check if the response contains any of the toxic keywords
        llm_toxicity = any(keyword in assistant_response for keyword in toxic_keywords)

        print(f"Assistant Response: {assistant_response}")
        print(f"Is Toxic: {llm_toxicity}")

        return llm_toxicity
    else:
        return f"Error: {response.status_code}, Response: {response.text}"


if __name__ == '__main__':
    app.run(debug=True)


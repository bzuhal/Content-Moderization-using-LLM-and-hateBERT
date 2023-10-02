# Flask API Documentation

This documentation provides an overview of the Flask API implemented in the provided code. The API serves two endpoints, `/api/moderate_hb` and `/api/moderate_llm`, both designed for text analysis purposes. The API utilizes various Python libraries and integrates with Prometheus for monitoring. Below, we describe the API, its endpoints, and the key functionality.

## Table of Contents

- [Dependencies](#dependencies)
- [Prometheus Metrics](#prometheus-metrics)
- [Endpoints](#endpoints)
  - [/api/moderate_hb](#api-moderate_hb)
  - [/api/moderate_llm](#api-moderate_llm)
- [Functions](#functions)
  - [hate_bt](#hate_bt)
  - [llm](#llm)
- [Running the API](#running-the-api)

## Dependencies<a name="dependencies"></a>

The following Python libraries are required to run this Flask API:

- `Flask`: A web microframework for building web applications.
- `flask_restx`: An extension for Flask to simplify the creation of RESTful APIs.
- `flasgger`: A tool for creating Swagger documentation for Flask APIs.
- `transformers`: A library for natural language understanding tasks using pre-trained models.
- `prometheus_flask_exporter`: An extension for Flask to expose Prometheus metrics.
- `prometheus_client`: A library for Prometheus metrics instrumentation.
- `requests`: A library for making HTTP requests.
- `psutil`: A library for retrieving system-related information.
- `os`: The Python standard library module for interacting with the operating system.

## Prometheus Metrics<a name="prometheus-metrics"></a>

This API utilizes Prometheus to collect and expose various metrics for monitoring and analysis. Some of the metrics include:

- `flask_memory_usage_bytes`: Measures the memory usage of the Flask process.
- `flask_method_calls`: Counts the number of method calls in the Flask app, categorized by HTTP method.
- `flask_request_duration_seconds`: Measures the time spent processing a request.

Metrics are exposed at the `/metrics` endpoint in Prometheus-compatible format.

## Endpoints<a name="endpoints"></a>

### /api/moderate_hb<a name="api-moderate_hb"></a>

- **Description**: This endpoint handles text moderation using the hateBERT model.
- **HTTP Method**: POST
- **Request Input**: JSON containing the `text` field, which is the text to be moderated.
- **Response Output**: JSON containing the moderation result.

#### Example Request:
```json
POST /api/moderate_hb
{
  "text": "This is a sample text to moderate."
}
```

#### Example Response:
```json
{
  "result": "The text 'This is a sample text to moderate.' is 'not_toxic' with a score of 0.987"
}
```

### /api/moderate_llm<a name="api-moderate_llm"></a>

- **Description**: This endpoint handles text moderation using a Language Model (LLM) from a remote API.
- **HTTP Method**: POST
- **Request Input**: JSON containing the `text` field, which is the text to be moderated.
- **Response Output**: JSON containing the moderation result.

#### Example Request:
```json
POST /api/moderate_llm
{
  "text": "This is another sample text to moderate."
}
```

#### Example Response:
```json
{
  "result": "This is another sample text to moderate. is not_toxic"
}
```

## Functions<a name="functions"></a>

### hate_bt(text)<a name="hate_bt"></a>

- **Description**: Analyzes text for toxicity using the hateBERT model.
- **Input**: `text` (str) - The text to be analyzed.
- **Output**: A dictionary containing the `label` and `score` of the text's toxicity.

### llm(comment, model, auth_token)<a name="llm"></a>

- **Description**: Analyzes text for toxicity using a Language Model (LLM) from a remote API.
- **Input**:
  - `comment` (str) - The text to be analyzed.
  - `model` (str) - The LLM model to use (default is "vicuna-33b-v1.3").
  - `auth_token` (str) - The authentication token for accessing the remote LLM API.
- **Output**: The toxicity analysis result as a string.

## Running the API<a name="running-the-api"></a>

To run the Flask API, execute the script. By default, it runs in debug mode.

```bash
python script_name.py
```

Replace `script_name.py` with the name of your Python script.

The API will be accessible locally, and you can interact with it using HTTP requests. Use the provided endpoints to perform text moderation tasks. Additionally, Prometheus metrics are exposed at `/metrics` for monitoring and analysis.
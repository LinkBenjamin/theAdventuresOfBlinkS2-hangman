from flask import Flask, jsonify
import requests
from prometheus_client import generate_latest, Counter, Histogram
import os, json

app = Flask(__name__)

# Ollama connection configuration
llm_uri = f"{os.getenv('LLM_URI')}/api/generate"
model_id = os.getenv("MODEL_ID")

REQUEST_COUNT = Counter('llm_requests_total', 'Total number of requests to the llm')
REQUEST_LATENCY = Histogram('llm_request_latency_seconds', 'Latency of requests to the llm')

@app.route('/metrics')
def metrics():
    return generate_latest()

@app.route('/getpuzzle', methods=['GET'])
def get_all_items():
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        try:
            prompt = "Suggest a Hangman puzzle I can use to defeat my friend. You may choose from these categories: 'thing', 'place', 'phrase', or 'food and drink'. Your puzzle must be more than three words long and less than ten words long.  You are required to respond with only the completed puzzle solution. What puzzle string should I use?"

            payload = {
                "model": model_id,
                "prompt": prompt
            }
            
            response = requests.post(llm_uri, json=payload)
            # Accumulate chunks for the puzzle solution
            full_response = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    full_response += chunk.get("response", "")
                    if chunk.get("done", False):
                        break

            # Parse the accumulated response as the puzzle solution
            result = full_response.strip().replace("\"", "").replace("'","")

            # Prepare a second request for the category hint
            payload_2 = {
                "model": model_id,
                "prompt": f"Given the possible categories of 'thing', 'place', 'phrase', or 'food and drink', What would be the most relevant category for the following hangman puzzle: << {result} >> ? You are required to answer with only the category."
            }

            response_2 = requests.post(llm_uri, json=payload_2)
            full_response_2 = ""
            for line in response_2.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    full_response_2 += chunk.get("response", "")
                    if chunk.get("done", False):
                        break

            # Parse the accumulated response as the category hint
            result_2 = full_response_2.strip().replace("\"", "").replace("'","")

            # Create the final JSON response
            final_response = {
                "hint": result_2,
                "phrase": result
            }
            return jsonify(final_response), 200

        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return jsonify({"error": "JSON decoding error"}), 500
        except Exception as e:
            print('Unable to connect to ollama port:', e)
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

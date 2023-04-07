import openai
from flask import Flask, request, jsonify
from utils import Terminal3
import os

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)

terminal3 = Terminal3(OPENAI_API_KEY=api_key,
                      model_selection='test', verbose=True)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    if not data or 'wallet_address' not in data or 'prompt' not in data:
        return jsonify({"error": "Invalid request. Provide wallet_address and prompt."}), 400

    wallet_address = data['wallet_address']
    prompt = data['prompt']

    try:
        answer = terminal3.start_new_chat(wallet_address, prompt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return answer

if __name__ == '__main__':
    app.run(debug=True, port=5000)
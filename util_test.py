import openai
from flask import Flask, request, jsonify
from utils import Terminal3
import os

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

api_key = ""

app = Flask(__name__)

terminal3 = Terminal3(OPENAI_API_KEY=api_key,
                      model_selection='test', verbose=True)

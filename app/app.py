from flask import request, jsonify, Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

## Routes

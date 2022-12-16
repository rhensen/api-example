from flask import Flask
from waitress import serve
import logging

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

app = Flask(__name__)

from routes import *

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)

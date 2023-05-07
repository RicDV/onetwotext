"""Module that expose onetwotext application"""

from os.path import *
import os
from flask import *
from waitress import serve
from onetwotext.word_calculator import *

_APP = Flask(__name__)


@_APP.route("/onetwotext", methods=["GET", "POST"])
def onetwotext():
    return render_template("onetwotext.html")


@_APP.route("/count-text", methods=["GET", "POST"])
def count_text():
    text = (request.json.get("text")).lower()
    response = python_count(text)
    return jsonify(response)


@_APP.route("/count-from-ai", methods=["GET", "POST"])
def count_from_ai():
    text = (request.json.get("text")).lower()
    response = nn_completion_count(text)
    return jsonify(response)


def start_app():
    serve(_APP, host="0.0.0.0", port=8000)

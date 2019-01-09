
from flask import Flask, request, jsonify, session, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#model = model_datastore


@app.route("/signin")
def signin():
    return True

@app.route("/join")
def join():
    return True




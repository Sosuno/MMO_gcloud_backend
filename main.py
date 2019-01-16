
from flask import Flask, request, jsonify, session, abort
from flask_cors import CORS
import db_control
app = Flask(__name__)
CORS(app)

#model = model_datastore
controller = db_control

@app.route("/signin", methods = ['POST'])
def signin():
    content = request.get_json()
    if content is None:
                return abort(400)
    result = controller.login(content)
    if result == False:
        return jsonify(msg = "Wrong username or password"), 403
    else:
        return result

@app.route("/join")
def join():
    return True





from flask import Flask, request, jsonify, session, abort
from flask_cors import CORS
import db_control
app = Flask(__name__)
CORS(app)


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

@app.route("/join", methods = ['POST'])
def join():
    content = request.get_json()
    if content is None:
                return abort(400)
    user = controller.register(content)
    if user is None:
        return jsonify("User already exists"), 403
    elif user == -1:
        return jsonify(msg = "No username"), 403
    result = controller.login(content)
    return result

@app.route("/game/worlds", methods = ['GET'])
def worlds():
    return True

@app.route("/game/<world>/init", methods = ['GET'])
def init_world(world):
    return True



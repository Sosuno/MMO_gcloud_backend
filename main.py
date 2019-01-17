
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
        return jsonify(msg = "No username"), 406
    result = controller.login(content)
    return result

@app.route("/game/worlds", methods = ['GET'])
def worlds():
    user = request_check(request)
    if user == -1:
        return abort(401)
    elif user == -2:
        return jsonify(msg = "Spierdoliam cos?"), 500
    worlds = controller.worlds.get_world()
    return jsonify(worldList = worlds)

@app.route("/game/create/<world>", methods = ['POST'])
def create_world(world):
    user = request_check(request)
    if user == -1:
        return abort(401)
    elif user == -2:
        return jsonify(msg = "Spierdoliam cos?"), 500
    if user['access'] == 'admin':
         world = db_control.create_world(world)
         return jsonify(newWorld = world)
    else:
        return jsonify(msg = "No access, sir"), 401

@app.route("/game/<world>/init", methods = ['GET'])
def init_world(world):
    user = request_check(request)
    if user == -1:
        return abort(401)
    elif user == -2:
        return jsonify(msg = "Spierdolilam cos?"), 500
    world = db_control.worlds.read_world(world)
    player = db_control.players.get_player(user['id'], world['id'])
    if player is None:
        player = join_world(world['id'], user, True)
        initWorld = {}
        initWorld['world'] = world
        initWorld['player'] = player
        #TODO not working
    return jsonify(initWorld = initWorld)

@app.route("/game/<world>/join", methods = ['GET'])
def join_world(world, user = None, noCheck = False):
    if not noCheck:
        user = request_check(request)
        if user == -1:
            return abort(401)
        elif user == -2:
            return jsonify(msg = "Spierdolilam cos?"), 500
        player = db_control.players.get_player(user['id'], world)
        if player is not None:
            init_world(world)
    data = {}
    data['username'] = user['username']
    data['world'] = world
    player = db_control.players.player_create(data)
    return jsonify(newPlayer = player)
    


def request_check(request):
    uuid = None
    if 'Authorization' not in request.headers:
        return -1
    uuid = request.headers.get('Authorization')
    if uuid is None:
        return -1
    if not db_control.session.check_if_session_active(uuid):
        return -1
    
    username = db_control.session.get_username_from_session(uuid)
    user = db_control.user.get_user(username)
    if user is None:
        return -2
    return user
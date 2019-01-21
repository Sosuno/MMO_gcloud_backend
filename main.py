
from flask import Flask, request, jsonify, session, abort
from flask_cors import CORS
import db_control
import re
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
        return jsonify(session = result)

@app.route("/join", methods = ['POST'])
def join():
    content = request.get_json()
    if content is None:
                return abort(400)
    if content.get('username') is None:
        return jsonify(msg = "No username"), 406
    user = controller.register(content)
    if user is None:
        return jsonify(msg = "User already exists"), 403
    elif user == -1:
        return jsonify(msg = "No username"), 406
    result = controller.login(content)
    return jsonify(session = result)

@app.route("/game/worlds", methods = ['GET'])
def worlds():
    user = request_check(request)
    if user == -1:
        return abort(401)
    elif user == -2:
        return jsonify(msg = "Spierdoliam cos"), 500
    worlds = controller.worlds.get_world()
    return jsonify(worldList = worlds)

@app.route("/game/create/<world>", methods = ['POST'])
def create_world(world):
    user = request_check(request)
    if user == -1:
        return abort(401)
    elif user == -2:
        return jsonify(msg = "Spierdoliam cos"), 500
    if user['access'] == 'admin':
         world = db_control.create_world(world)
         return jsonify(newWorld = world)
    else:
        return jsonify(msg = "No access, sir"), 401

@app.route("/game/worlds/<worldId>", methods = ['GET'])
def init_world(worldId):
    user = request_check(request)
    if user == -1:
        return abort(401)
    elif user == -2:
        return jsonify(msg = "Spierdolilam cos"), 500
    world = db_control.worlds.read_world(worldId) 
    return jsonify(World = world)

@app.route("/game/<world>/join", methods = ['POST'])
def join_world(world, user = None, noCheck = False):
    if not noCheck:
        user = request_check(request)
        if user == -1:
            return abort(401)
        elif user == -2:
            return jsonify(msg = "Spierdolilam cos"), 500
        player = db_control.players.get_player(user['id'], world)
        if player is not None:
            return jsonify(msg = "Already in")
    data = {}
    data['username'] = user['username']
    data['world'] = world
    data['userId'] = user['id']
    player = db_control.players.player_create(data)
    if player == -1:
        return jsonify(msg = "World is full"), 406
    return jsonify(newPlayer = player)

@app.route("/game/player/<world>", methods = ['GET'])
def get_player(world):
    user = request_check(request)
    if user == -1:
        return abort(401)
    elif user == -2:
        return jsonify(msg = "Spierdolilam cos"), 500
    player = db_control.players.get_player(user['id'], world)
    if player is None:
        return abort(406)
    if 'userId' in player:
        del player['userId']
    return jsonify(player = player)

@app.route("/game/profile/<playerId>/", methods = ['GET'])
def get_player_profile(playerId):
    user = request_check(request)
    if user == -1:
        return abort(401)
    elif user == -2:
        return jsonify(msg = "Spierdolilam cos"), 500
    w = int(re.search(r'\d+', playerId).group())
    player = db_control.players.player_read(w)
    if player is None:
        return jsonify(msg = "I am potato", id = w)
    returnPlayer = {}
    returnPlayer['username'] = player['username']
    returnPlayer['avatarURL'] = user['avatarURL']

    return jsonify(player = returnPlayer)

@app.route("/game/player/world/attack", methods = ['POST'])
def attack_square():
    user = request_check(request)
    if user == -1:
        return abort(401)
    elif user == -2:
        return jsonify(msg = "Coś nie działa"), 500
    content = request.get_json()
    if content is None:
                return abort(400)
    if content.get('playerid') is None:
        return jsonify(msg = "No player id"), 406
    if content.get('squareid') is None:
        return jsonify(msg = "No square id"), 406
    if content.get('bullets') is None:
        return jsonify(msg = "Bullet amount undefined"), 406
    bullets = content.get('bullets')
    player = db_control.players.player_read(content.get('playerid'))
    square = db_control.worldMap.read_square(content.get('squareid'))
    if player['world'] != square['world']:
        return jsonify(msg = "Player is in world" + str(square['world']) + ", square is in " + str(player['world'])), 408

    return jsonify(msg = db_control.attack(player,square,bullets))
    
@app.route("/game/cron")
def calculate_world():


    return None

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

from flask import Flask, request, jsonify, session, abort
from flask_cors import CORS
import world_calculations
import db_control
import admin_functions
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
        return jsonify(msg = "No access, sir"), 403

@app.route("/game/worlds/<worldId>", methods = ['GET'])
def init_world(worldId):
    user = request_check(request)
    if user == -1:
        return abort(401)
    elif user == -2:
        return jsonify(msg = "Spierdolilam cos"), 500
    id = None
    world = db_control.worlds.read_world(worldId) 
    player = db_control.players.get_player(user['id'], worldId)
    if player is not None:
        id = player['id']
    return jsonify(World = world, playerId = id)

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
            return jsonify(msg = "Already in"), 403
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
    
    return jsonify(player = player, buildings = controller.get_player_upgrade_cost(player['id']), 
    pending = controller.generate_pending(world, player['id']),
    toRaport = controller.generate_raports(world, player['id'])
    )

@app.route("/game/profile/<playerId>/", methods = ['GET'])
def get_player_profile(playerId):
    user = request_check(request)
    if user == -1:
        return abort(401)
    elif user == -2:
        return jsonify(msg = "Spierdolilam cos"), 500
    player = db_control.players.player_read(playerId)
    if player is None:
        return abort(406)
    returnPlayer = {}
    returnPlayer['username'] = player['username']
    returnPlayer['avatarURL'] = user['avatarURL']

    return jsonify(player = returnPlayer)

@app.route("/game/attack", methods = ['POST'])
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
    if int(player['world']) != int(square['world']):
        return jsonify(msg = "Player is in world" + str(square['world']) + ", square is in " + str(player['world'])), 408

    result, error = controller.attack(player,square,bullets)
    if error == -1:
        return jsonify(msg = result), 406

    return jsonify(msg = result)
    
@app.route("/game/cron", methods = ['GET'])
def calculate_world():
    
    if not request.headers.get("X-Appengine-Cron"):
        user = request_check(request)
        if user == -1:
            abort(403)
        if user['access'] != 'admin':
            abort(403)
        
    worlds = controller.worlds.get_world(None, 'name')
    for world in worlds:
        
        world_calculations.calculate_world(world['id'])
    
    return jsonify(msg = "Done")


@app.route("/session", methods = [ 'GET' , 'DELETE' ])
def sessions():
    user = request_check(request)
    if user == -1:
        return jsonify(session = False)
    elif user == -2:
        return jsonify(msg = "Spierdolilam cos"), 500
    uuid = request.headers.get('Authorization')
    if request.method == 'GET':
        if not db_control.session.check_if_session_active(uuid):
            return jsonify(session = False)
        else:
            return jsonify(session = True)
    else:
        if not db_control.session.check_if_session_active(uuid):
            return jsonify(msg = "No session")
        db_control.session.destroy_all_user_sessions(uuid)
        return jsonify(msg = "Deleted")

@app.route("/game/upgrade/<playerId>/<buildingId>/", methods = ['POST'])
def upgrade_building(playerId,buildingId):
    #sprawdzenie czy regquest jest wyslany przez zalogowanego uzytkownika
    user = request_check(request)
    if user == -1:
        return abort(401)
    elif user == -2:
        return jsonify(msg = "Spierdolilam cos"), 500
   
    updatingPlayersResources, lack= db_control.upgrade_building(playerId,buildingId)
    if updatingPlayersResources == -1:
        return abort(406)
    
    if lack == -1:
        return jsonify(fail=updatingPlayersResources),406
    return jsonify(player = updatingPlayersResources)
    
@app.route("/game/<world>/generate/raports", methods = ['GET'])
def generate_raports(world):
    user = request_check(request)
    if user == -1:
        return abort(401)
    elif user == -2:
        return jsonify(msg = "Spierdolilam cos"), 500
    player = controller.players.get_player(user['id'], world)

    return jsonify(pendingRaports = controller.generate_pending(world, player['id']), toRaports = controller.generate_raports(world, player['id']))
    
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




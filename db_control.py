from db import buildings, players, user, worldMap, worlds, timestamps, session, database
from flask import jsonify

def login(data):
    
    if data is None:
        return False
    if data.get('username') is None:
        return False
    if data.get('password') is None:
        return False
    if user.is_correct_user(data['username'], data['password']):
            session.destroy_all_user_sessions(data['username'])
            my_session = session.create_session(data['username'])
            return my_session['sessionID']
    else:
        return False

def register(data):
        username = data['username'].strip()
        if not username:
                return -1
        if not user.is_user_in_db(username):
                newUser = user.user_create(data)
                return newUser
        else:
                return None

def create_world(name, size = 25, capacity = 4):
        world = worlds.create_world(name, size, capacity)
        return world

def attack(player,status,bullets):
        
    if player['actionPoints'] < 5:
        return "Not enough action points"
    elif player['naboje'] < 100:
        return "Not enough bullets"
    elif player['naboje'] < bullets:
        return "Not enough bullets"
    else:
        player['naboje'] = player['naboje'] - 100
        player['actionPoints'] = player['actionPoints'] - 5
        players.player_update(player, player['id'])
         # todo - add attack action to cron
        if status == "free":
            return "Taking over commenced. You used 5 action points."
        elif status == "occupied":
            return "Attacking enemy territory commenced. You used 5 action points."
        elif status == "city":
            return "Attacking enemy city commenced. You used 5 action points."
        else:
            return "Unable to get field status"
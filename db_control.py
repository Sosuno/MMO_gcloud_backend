from db import buildings, players, user, worldMap, worlds, timestamps, session, database

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



def create_buildings():
        data = {}
        data['name'] = 'Lumber Mill'
        data['lvl'] = 1
        data['woodCost'] = 0
        data['capsCost'] = 0
        data['pointsCost'] = 0
        data['income'] = 50
        
        buildings.create_building(data)

        data['name'] = 'Lumber Mill'
        data['lvl'] = 2
        data['woodCost'] = 3000
        data['capsCost'] = 1000
        data['pointsCost'] = 3
        data['income'] = 150
        
        buildings.create_building(data)

        data['name'] = 'Lumber Mill'
        data['lvl'] = 3
        data['woodCost'] = 10000
        data['capsCost'] = 3000
        data['pointsCost'] = 3
        data['income'] = 300
        
        buildings.create_building(data)

        data['name'] = 'Armory'
        data['lvl'] = 1
        data['woodCost'] = 0
        data['capsCost'] = 0
        data['pointsCost'] = 0
        data['income'] = 50
        
        buildings.create_building(data)

        data['name'] = 'Armory'
        data['lvl'] = 2
        data['woodCost'] = 3200
        data['capsCost'] = 1500
        data['pointsCost'] = 4
        data['income'] = 180
        
        buildings.create_building(data)

        data['name'] = 'Armory'
        data['lvl'] = 3
        data['woodCost'] = 11000
        data['capsCost'] = 3400
        data['pointsCost'] = 4
        data['income'] = 500
        
        buildings.create_building(data)

        data['name'] = 'Bank'
        data['lvl'] = 1
        data['woodCost'] = 0
        data['capsCost'] = 0
        data['pointsCost'] = 0
        data['income'] = 50
        
        buildings.create_building(data)

        data['name'] = 'Bank'
        data['lvl'] = 2
        data['woodCost'] = 3000
        data['capsCost'] = 3000
        data['pointsCost'] = 4
        data['income'] = 250
        
        buildings.create_building(data)

        data['name'] = 'Bank'
        data['lvl'] = 3
        data['woodCost'] = 5000
        data['capsCost'] = 7500
        data['pointsCost'] = 4
        data['income'] = 400
        
        buildings.create_building(data)

        data['name'] = 'Bunker'
        data['lvl'] = 1
        data['woodCost'] = 0
        data['capsCost'] = 0
        data['pointsCost'] = 0
        data['income'] = 1
        
        buildings.create_building(data)

        data['name'] = 'Bunker'
        data['lvl'] = 2
        data['woodCost'] = 3000
        data['capsCost'] = 3000
        data['pointsCost'] = 4
        data['income'] = 1.2
        
        buildings.create_building(data)

        data['name'] = 'Bunker'
        data['lvl'] = 3
        data['woodCost'] = 5000
        data['capsCost'] = 8000
        data['pointsCost'] = 4
        data['income'] = 1.8
        
        buildings.create_building(data)

        data['name'] = 'Pantry'
        data['lvl'] = 1
        data['woodCost'] = 0
        data['capsCost'] = 0
        data['pointsCost'] = 0
        data['income'] = 50
        
        buildings.create_building(data)

        data['name'] = 'Pantry'
        data['lvl'] = 2
        data['woodCost'] = 2000
        data['capsCost'] = 1500
        data['pointsCost'] = 4
        data['income'] = 150
        
        buildings.create_building(data)

        data['name'] = 'Pantry'
        data['lvl'] = 3
        data['woodCost'] = 4000
        data['capsCost'] = 4000
        data['pointsCost'] = 4
        data['income'] = 300
        
        buildings.create_building(data)

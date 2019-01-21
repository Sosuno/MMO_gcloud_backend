from db import buildings, players, user, worldMap, worlds, timestamps, session, database, actions

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

def upgrade_building(playerId, buildingId):
        #pobranie obiektu z bazy danych po ID
        currentBuilding = buildings.building_read(buildingId)
        player = players.player_read(playerId)
        if currentBuilding['lvl']==3:
                return -1, None
        if currentBuilding == None:
                return -1, None
        
        if player == None:
                return -1, None
        upgradedBuilding = buildings.get_buildings(currentBuilding['name'],currentBuilding['lvl']+1).pop() #jaki ma byc po upgradzie
        
       
        #czy playera stac na budynek 
        #woodcost
        check={}
        bool = False
        #jezeli budynek jest na poziomie 3 to ma najwyzszy lvl
        if upgradedBuilding['woodCost']> player['deski']:
                check['deski']='0'
                bool= True
        else:
                check['deski']='1'
        #capscost
        if upgradedBuilding['capsCost'] >player['kapsle']:
                check['kapsle']='0'
                bool= True
        else:
                 check['kapsle']='1'
        #points
        if upgradedBuilding['pointsCost']>player['actionPoints']:
                check['actionPoints']='0'
                bool= True
        else:
                 check['actionPoints']='1'
        #jezeli ktoregos surowca jest za malo,albo budynek jest na najwyzszym poziomie
        if bool==True:
                return check, -1
        #jezeli wszysto sie zgadza
        player['deski']= player['deski']-upgradedBuilding['woodCost']
        player['kapsle']= player['kapsle']-upgradedBuilding['capsCost']
        player['pointsCost']= player['actionPoints']-upgradedBuilding['pointsCost']
        sendToActonTable={}
        sendToActonTable['player']=player['id']
        sendToActonTable['status']='uncompleted'
        sendToActonTable['building']=currentBuilding['name']
        sendToActonTable['action']='buildingUpgrade'
        sendToActonTable['world']=player['world']
        updatedplayer= players.player_update(player,player['id'])
        actions.create_action(sendToActonTable)
        return updatedplayer, None


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

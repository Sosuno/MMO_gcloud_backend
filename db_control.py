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
def generate_resources(playerId):
        player = players.player_read(playerId)

        tartak = buildings.building_read(player['tartakId'])
        bunkier = buildings.building_read(player['bunkierId'])
        bank = buildings.building_read(player['bankId'])
        sklad = buildings.building_read(player['skladId'])
        spizarnia= buildings.building_read(player['spizarniaId'])
#trzeba dodac bonus za tereny
        player['deski']=(player['deski']+tartak['income'])* bunkier['income']*((1+player['actionPoints']) * 0.12)
        player['kapsle']=(player['kapsle']+bank['income'])* bunkier['income']*((1+player['actionPoints']) * 0.12)
        player['naboje']=(player['naboje']+sklad['income'])* bunkier['income']*((1+player['actionPoints']) * 0.12)
        player['jagody']=(player['jagody']+spizarnia['income'])* bunkier['income']*((1+player['actionPoints']) * 0.12)
        updatedplayer= players.player_update(player,player['id'])
        return updatedplayer


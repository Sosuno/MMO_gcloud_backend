from db import buildings, players, user, worldMap, worlds, timestamps, session, database, actions,logs


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
            logs.create_login_log(data['username'])
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

def get_player_upgrade_cost(playerid):
        player = players.player_read(playerid)
        builds = {}
        if player['tartak'] != 3:
                lumberMill = buildings.get_buildings('Lumber Mill', player['tartak']+1).pop() 
        else:
                lumberMill = 'max'
        builds['lumberMill']  = lumberMill

        if player['sklad'] != 3:
                armory = buildings.get_buildings('Armory', player['sklad']+1).pop() 
        else:
                armory = 'max'
        builds['armory'] = armory

        if player['sejf'] != 3:
                bank = buildings.get_buildings('Bank', player['sejf']+1).pop() 
        else:
                bank = 'max'
        builds['bank'] = bank

        if player['spizarnia'] != 3:
                pantry = buildings.get_buildings('Pantry', player['spizarnia']+1).pop() 
        else:
                pantry = 'max'
        builds['pantry'] = pantry

        if player['bunkier'] != 3:
                bunker = buildings.get_buildings('Bunker', player['bunkier']+1).pop() 
        else:
                bunker = 'max'
        builds['bunker'] = bunker
        return builds
        
def attack(player,square,bullets):
        
    status = square['status']

    if player['actionPoints'] < 5:
        return "Not enough action points", -1
    elif player['naboje'] < 100:
        return "Not enough bullets", -1
    elif int(player['naboje']) < int(bullets):
        return "Not enough bullets. You currently have " + str(player['naboje']) + ".", -1
    elif player['id'] == square['owner']:
        return "You cannot attack your own territory", -1
    else:
        player['naboje'] = int(player['naboje']) - int(bullets)
        player['actionPoints'] = int(player['actionPoints']) - 5
        player = players.player_update(player, player['id'])
   
        data = {}
        data['player'] = player['id']
        data['square'] = square['id']
        data['world'] = player['world']
        data['bullets'] = bullets
        data['status'] = 'uncompleted'
        

         # todo - add attack action to cron
        if status == "free":
            data['action'] = "take"
            actions.create_action(data)
            return "Taking over commenced. You used 5 action points.", 0
        elif status == "occupied":
            data['action'] = "take over"
            actions.create_action(data)
            return "Attacking enemy territory commenced. You used 5 action points.", 0
        elif status == "City":
            data['action'] = "attack"
            actions.create_action(data)
            return "Attacking enemy city commenced. You used 5 action points.", 0
        else:
            return "Unable to get field status", -1

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
        player['actionPoints']= player['actionPoints']-upgradedBuilding['pointsCost']
        sendToActonTable={}
        sendToActonTable['player']=player['id']
        sendToActonTable['status']='uncompleted'
        sendToActonTable['building']=currentBuilding['name']
        sendToActonTable['action']='buildingUpgrade'
        sendToActonTable['world']=player['world']
        updatedplayer= players.player_update(player,player['id'])
        actions.create_action(sendToActonTable)
        return updatedplayer, None

def generate_pending(worldId, playerId):
        pending = actions.get_uncompleted_actions(worldId, None, playerId)
        pendingList = []
        for rap in pending:
                text = "You are "
                if rap['action'] == 'buildingUpgrade':
                        text = text + "upgrading " + rap['building']
                elif rap['action'] == 'take':
                        text = text + "trying to occupy territory"
                elif rap['action'] == 'take over':
                        text = text + "trying to take over a territory"
                elif rap['action'] == 'attack':
                        text = text + "trying to attack a city"
                pendingList.append(text)

        return pendingList


def generate_raports(worldId, playerId):
        toReport = actions.get_to_report_actions(worldId, playerId)
        rapList = []
        defendToReport = actions.get_defended_actions(worldId,playerId)
        for rap in toReport:
                text = "You have "
                if rap['action'] == 'buildingUpgrade':
                        text = text + "upgraded " + rap['building']
                elif rap['action'] == 'take':
                        if rap['outcome'] == 'fail':
                                text = text + "failed in attempt to occupy territory. Take more bullets next time"
                        else:
                                text = text + "successfully taken a territory"
                elif rap['action'] == 'take over':
                        if rap['outcome'] == 'fail':
                                text = text + "failed in attempt to take over a territory. Take more bullets next time"
                        else:
                                text = text + "successfully taken over a territory"
                elif rap['action'] == 'attack':
                        if rap['outcome'] == 'fail':
                                text = text + "failed in attempt to attack the city. Take more bullets next time"
                        else:
                                spoils = rap['spoils']
                                text = "Your attack was a succes. " + text + "You have taken " + spoils['wood'] + " wood, "
                                text = text + spoils['berries'] + " berries, " + spoils['caps'] + " caps. Well done!"
                rapList.append(text)

        for defend in defendToReport:
                if defend['action'] == 'take over':
                        if defend['outcome'] == 'fail':
                                text = "You have successfully defended your territory"
                        else:
                                text = "You have lost a battle for your territory. It was taken by another player"
                elif defend['action'] == 'attack':
                        if defend['outcome'] == 'fail':
                                text = "You have successfully defended your territory"
                        else:
                                spoils = defend['spoils']
                                text = "Your attack city was attacked and you were out of bullets. " + text + "You have lost " + spoils['wood'] + " wood, "
                                text = text + spoils['berries'] + " berries, " + spoils['caps'] + " caps."
                rapList.append(text)

        return rapList
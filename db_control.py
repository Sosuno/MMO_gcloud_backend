from db import buildings, players, user, worldMap, worlds, timestamps, session, database, actions
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
        data['player1'] = player['id']
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

def generate_resources(playerId):
        player = players.player_read(playerId)
        terytory_status= len(worldMap.get_square_status(player['world'], 'occupied', player['id']))

        tartak = buildings.building_read(player['tartakId'])
        bunkier = buildings.building_read(player['bunkierId'])
        bank = buildings.building_read(player['sejfId'])
        sklad = buildings.building_read(player['skladId'])
        spizarnia= buildings.building_read(player['spizarniaId'])
#trzeba dodac bonus za tereny
        player['deski']= player['deski'] + (tartak['income'] * bunkier['income']*(1+player['actionPoints']) * 0.10) * (1 + terytory_status * 0.15)
        player['kapsle']=player['kapsle'] + (bank['income'] * bunkier['income']*(1+player['actionPoints']) * 0.10) * (1 + terytory_status * 0.15)
        player['naboje']=player['naboje'] + (sklad['income'] * bunkier['income']*(1+player['actionPoints']) * 0.10) * (1 + terytory_status * 0.15)
        player['jagody']=player['jagody'] + (spizarnia['income'] * bunkier['income']*(1+player['actionPoints']) * 0.10) * (1 + terytory_status * 0.15)
        player['actionPoints'] = 10
        updatedplayer= players.player_update(player,player['id'])
        return updatedplayer

def calculate_world(world):

        oldActions = actions.get_to_report_actions(world)
        contestedSquares = []
        for action in oldActions:
                action['status'] = 'completed'
                actions.update_action(action, action['id'])

        actionList = actions.get_uncompleted_actions(world)
        for action in actionList:
                if action[square] in contestedSquares:
                        continue
                player = players.player_read(action['player'])
                if action['action'] == 'buildingUpgrade':
                        if action['building'] == 'Bank':
                                player['bank'] = player['bank'] +1
                        if action['building'] == 'Armory':
                                player['sklad'] = player['sklad'] +1
                        if action['building'] == 'Pantry':
                                player['spizarnia'] = player['spizarnia'] +1
                        if action['building'] == 'Bunker':
                                player['bunkier'] = player['bunkier'] +1
                        if action['building'] == 'Lumber Mill':
                                player['tartak'] = player['tartak'] +1
                        player = players.player_update(player, player['id'])
                        action['status'] = 'To report'
                        action['data'] = timestamps.current_date()
                        actions.update_action(action, action['id'])
                elif action['action'] == 'take':
                        square = worldMap.read_square(action['square'])
                        check = actions.check_if_double_take(square)
                        if check == False:
                                square['owner'] = player['id']
                                square['status'] = 'occupied'
                                worldMap.update_square(square, square['id'])
                                action['status'] = 'To report'
                                actions.update_action(action, action['id'])
                        else:
                                contestedSquares.append(square['id'])
                                fight(check, square)
                elif action['action'] == 'take over':
                        take_over(action,player)
                elif action['action'] == 'attack':
                        attack_action(action,player)

        playersList = players.get_players()
        for player in playersList:
                generate_resources(player)
                   
def take_over(action, player1):
        square = worldMap.read_square(action['square'])
        player2 = players.player_read(square['owner'])
        action['status'] = 'To report'
        action['player2'] = player2['id']
        if action['bullets'] <= player2['naboje']:
                action['outcome'] = 'fail'
                player2['naboje'] = player2['naboje'] - action['bullets']
                player2 = players.player_update(player2,player2['id'])
        else:
                action['outcome'] = 'success'
                player2['naboje'] = 0
                square['owner'] = player1['id']
                player2 = players.player_update(player2,player2['id'])
                worldMap.update_square(square, square['id'])
        actions.update_action(action, action['id'])
        
def attack_action(action, player1):
        square = worldMap.read_square(action['square'])
        player2 = players.player_read(square['owner'])
        action['status'] = 'To report'
        action['player2'] = player2['id']
        if action['bullets'] <= player2['naboje']:
                action['outcome'] = 'fail'
                player2['naboje'] = player2['naboje'] - action['bullets']
        else:
                action['outcome'] = 'success'
                player2['naboje'] = 0
                wood = 0.15 * player2['deski']
                caps = 0.15 * player2['kapsle']
                berries = 0.15 * player2['jagody']
                player1['deski'] = wood
                player1['jagody'] = berries
                player1['kapsle'] = caps

                player2['deski'] = player2['deski'] - wood
                player2['jagody'] = player2['jagody'] - berries
                player2['kapsle'] = player2['kapsle'] - caps
                action['spoils'] = {
                                "berries": berries,
                                "caps": caps,
                                "wood": wood
                                }
                
        player2 = players.player_update(player2,player2['id'])
        player1 = players.player_update(player1,player1['id'])
        actions.update_action(action, action['id'])
        
def fight(square, fights):
        maxBid = -1
        maxBidder = None
        tie = None
        for fight in fights:
                if fight['bullets'] > maxBid:
                        maxBidder = fight['player']

        for fight in fights:                        
                if fight['bullets'] == maxBid and fight['player'] != maxBidder:
                        tie = True

        if not tie:
                square['owner'] = maxBidder
                square['status'] = 'occupied'
                worldMap.update_square(square, square['id'])

        for fight in fights:
                fight['outcome'] = 'fail'
                fight['status'] = 'To report'
                fight['multi'] = True

                if not tie:
                        if fight['player'] == maxBidder:
                                fight['outcome'] = 'success'

                actions.update_action(fight,fight['id'])
                



        
        
from db import buildings, players, user, worldMap, worlds, timestamps, session, database, actions

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

        session.invalidate_all_user_sessions()
        oldActions = actions.get_to_report_actions(world)
        contestedSquares = []
        for action in oldActions:
                action['status'] = 'completed'
                actions.update_action(action, action['id'])

        actionList = actions.get_uncompleted_actions(world)
        #return actionList
        for action in actionList:
                action['data'] = timestamps.current_date()
                if 'square' in action:
                        if action['square'] in contestedSquares:
                                continue
                if 'player' in action:
                        player = players.player_read(action['player'])
                else:
                        player = players.player_read(action['player1'])
                if action['action'] == 'buildingUpgrade':
                        if action['building'] == 'Bank':
                                player['sejf'] = player['sejf'] +1
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
                        actions.update_action(action, action['id'])
                elif action['action'] == 'take':
                        square = worldMap.read_square(action['square'])
                        check = actions.check_if_double_take(square['id'])
                        if check == False:
                                square['owner'] = player['id']
                                square['status'] = 'occupied'
                                worldMap.update_square(square, square['id'])
                                action['status'] = 'To report'
                                action['outcome'] = 'success'
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
                generate_resources(player['id'])

                   
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


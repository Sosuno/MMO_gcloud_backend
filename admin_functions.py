from db import buildings, players, user, worldMap, worlds, timestamps, session, database

def update_users():
        playersList = players.get_players()

        for player in playersList:
                player['tartakId'] = 6571545078005760
                player['sejfId'] = 6197949226811392 
                player['skladId'] = 6479330687320064
                player['spizarniaId'] = 5798449991647232 
                player['bunkierId'] = 5259355528101888
                players.player_update(player, player['id'])

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

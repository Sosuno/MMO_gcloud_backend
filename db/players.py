#import database
from .database import get_client,get_entity, datastore
from .timestamps import current_timestamp
from .worldMap import get_square_status, update_square
from .worlds import read_world, update_world

import random



def get_player(userId, world):
    ds = get_client()
    query = ds.query(kind = 'Player')
    query.add_filter('userId', '=', userId)
    query.add_filter('world', '=', world)
    result = list(query.fetch())
    
    if result is None:
        return None
    elif not result:
        return None
    r = result.pop()
    return get_entity(r)

def player_read(id):
    ds = get_client()
    key = ds.key('Player', int(id))
    results = ds.get(key)
    result = get_entity(results)
    return result

def player_create(data):
    world = read_world(data['world'])
    if 'players' not in world:
        world['players'] = 0
    elif world['capacity'] == world['players']:
        return -1
    freeSquares = get_square_status(data['world'])
    if freeSquares == None:
        return -1
    world['players'] = world['players'] + 1
    world = update_world(world, world['id'])

    ds = get_client()
    key = ds.key('Player')
    entity = datastore.Entity(
        key=key,
    )
    data['deski'] = 1000
    data['kapsle'] = 1000
    data['naboje'] = 1000
    data['jagody'] = 1000
    data['tartak'] = 1
    data['tartakId'] = 6571545078005760
    data['sejf'] = 1
    data['sejfId'] = 6197949226811392
    data['sklad'] = 1
    data['skladId'] = 6479330687320064
    data['spizarnia'] = 1
    data['spizarniaId'] = 5798449991647232 
    data['bunkier'] = 1
    data['bunkierId'] = 5259355528101888
    data['actionPoints'] = 10
    data['lastLogin'] = current_timestamp()
    entity.update(data)
    ds.put(entity)
    player = get_entity(entity)

    base = random.choice(freeSquares)
    base['status'] = 'City'
    base['owner'] = player['id']
    update_square(base, base['id'])
    if 'userId' in player:
        del player['userId']
    return player

def player_update(data, id):
    ds = get_client()
    key = ds.key('Player', int(id))
    entity = datastore.Entity(
        key=key,
        )
    if 'id' in data:
        del data['id']
    entity.update(data)
    ds.put(entity)
    return get_entity(entity)


def get_players():
    ds = get_client()
    query = ds.query(kind = 'Player')

    results = []
    
    for entity in query.fetch():
            results.append(get_entity(entity))

    return results
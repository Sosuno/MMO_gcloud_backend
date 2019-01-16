#import database
from .database import get_client,get_entity, datastore
from .timestamps import current_timestamp





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
    return get_entity(results)

def player_create(data):
    ds = get_client()
    key = ds.key('Player')
    entity = datastore.Entity(
        key=key,
    )
    #TODO surowce i początkowy stan bazy - do ustalenia
    data['res1'] = 1000
    data['res2'] = 1000
    data['res3'] = 1000
    data['build1'] = 1
    data['build2'] = 1
    data['build3'] = 1
    data['actionPoints'] = 10
    data['lastLogin'] = current_timestamp()
    entity.update(data)
    ds.put(entity)
    return get_entity(entity)

def player_update(data,id):
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

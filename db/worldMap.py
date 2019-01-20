from .database import get_client,get_entity, datastore
from .timestamps import current_timestamp
import re


def get_map(world):
    ds = get_client()
    query = ds.query(kind = 'Map')
    query.add_filter('world', '=', world)
    results = []
    for entity in query.fetch():
        results.append(get_entity(entity))

    return results

def read_square(id):
    ds = get_client()
    key = ds.key('Map', int(id))
    result = ds.get(key)
    return get_entity(result)

def get_square_status(world, status = 'free'):

    w = int(re.search(r'\d+', world).group())
    ds = get_client()
    query = ds.query(kind = 'Map')
    query.add_filter('status', '=', status)
    query.add_filter('world', '=', w)
    results = []
    for entity in query.fetch():
        results.append(get_entity(entity))
    return results

def update_square(square, id):
    ds = get_client()
    key = ds.key('Map', int(id))
    entity = datastore.Entity(
        key=key,
        )
    if 'id' in square:
        del square['id']
    entity.update(square)
    ds.put(entity)
    return get_entity(entity)
    
def create_map(world, size):
    ds = get_client()
    i = 0
    map = []
    cordX = 1
    cordY = 0
    while i < size:
        if cordY == 5:
            cordY = 1
            cordX += 1
        else:
            cordY += 1
        i += 1
        key = ds.key('Map')
        entity = datastore.Entity(
        key=key,
        )
        data = {}
        data['world'] = world
        data['owner'] = 'None'
        data['status'] = 'free'
        data['num'] = i
        data['cordX'] = cordX
        data['cordY'] = cordY
        entity.update(data)
        ds.put(entity)
        map.append(get_entity(entity))

    return map

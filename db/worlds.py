from .worldMap import get_map, create_map
from .database import get_client,get_entity, datastore
from .timestamps import current_timestamp




def read_world(id):
    ds = get_client()
    key = ds.key('World', int(id))
    results = ds.get(key)
    world = get_entity(results)
    world['map'] = get_map(world['id'])
    return world


def get_world(name = None, projection = None):
    ds = get_client()
    query = ds.query(kind = 'World')
    if projection is not None:
         query.projection = [projection]
    if name is not None:
        query.add_filter('name', '=', name)
    else:
        results = []
    
    for entity in query.fetch():
        if name is not None:
            results = get_entity(entity)
            results['map'] = get_map(results['id'])
        else:
            results.append(get_entity(entity))

    return results

def create_world(name, size, capacity):
    ds = get_client()
    key = ds.key('World')
    entity = datastore.Entity(
        key=key,
    )

    data = {}
    data['name'] = name
    data['size'] = size
    data['capacity'] = capacity
    data['players'] = 0
    data['map'] = None
    data['created'] = current_timestamp()
    data['endDate'] = None
    entity.update(data)
    ds.put(entity)
    world = get_entity(entity)
    world['map'] = create_map(world['id'], size)
    return world

    
def update_world(world, id):
    ds = get_client()
    key = ds.key('World', int(id))
    entity = datastore.Entity(
        key=key,
        )
    if 'id' in world:
        del world['id']
    entity.update(world)
    ds.put(entity)
    return get_entity(entity)
from .worldMap import get_map
from .database import get_client,get_entity, datastore
from .timestamps import current_timestamp




def read_world(id):
    ds = get_client()
    key = ds.key('World', int(id))
    results = ds.get(key)
    return get_entity(results)


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


    

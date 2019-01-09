import worldMap
import database
import timestamps


time = timestamps
db = database
worldMap = worldMap


def read_world(id):
    ds = db.get_client()
    key = ds.key('World', int(id))
    results = ds.get(key)
    return db.get_entity(results)


def get_world(name = None, projection = None):
    ds = db.get_client()
    query = ds.query(kind = 'World')
    if projection is not None:
         query.projection = [projection]
    if name is not None:
        query.add_filter('name', '=', name)
    else:
        results = []
    
    for entity in query.fetch():
        if name is not None:
            results = db.get_entity(entity)
            results['map'] = worldMap.get_map(results['id'])
        else:
            results.append(db.get_entity(entity))

    return results


    

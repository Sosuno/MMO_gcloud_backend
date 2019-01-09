import database
import timestamps

time = timestamps
db = database

def get_buildings(name = None, lvl = None, projection = None):
    ds = db.get_client()
    query = ds.query(kind = 'Building')
    if projection is not None:
        query.projection = [projection]
    if name is not None:
        query.add_filter('name', '=', name)
    if lvl is not None:
        query.add_filter('lvl', '=', lvl)
    result = []

    for entity in query.fetch():
            result.append(db.get_entity(entity))
            

    if result is None:
        return None
    elif not result:
        return None
    return result

def create_building(data):
    ds = db.get_client()
    key = ds.key('Building')
    entity = db.datastore.Entity(
        key=key,
    )
    entity.update(data)
    ds.put(entity)

def update_building(data, id):
    ds = db.get_client()
    key = ds.key('Building', int(id))
    entity = db.datastore.Entity(
        key=key,
        )
    if 'id' in data:
        del data['id']
    entity.update(data)
    ds.put(entity)
    return db.get_entity(entity)

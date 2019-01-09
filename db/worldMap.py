import database

db = database

def get_map(world):
    ds = db.get_client()
    query = ds.query(kind = 'Map')
    query.add_filter('world', '=', world)
    results = []
    for entity in query.fetch():
        results.append(db.get_entity(entity))

    return results

def read_square(id):
    ds = db.get_client()
    key = ds.key('Map', int(id))
    result = ds.get(key)
    return db.get_entity(result)

def update_sqare(square, id):
    ds = db.get_client()
    key = ds.key('Map', int(id))
    entity = db.datastore.Entity(
        key=key,
        )
    if 'id' in square:
        del square['id']
    entity.update(square)
    ds.put(entity)
    return db.get_entity(entity)
    
def create_map(world, size):
    ds = db.get_client()
    i = 0
    map = []
    while i < size:
        i += 1
        key = ds.key('Map')
        entity = db.datastore.Entity(
        key=key,
        )
        data = {}
        data['world'] = world
        data['owner'] = 'None'
        data['status'] = 'free'
        entity.update(data)
        ds.put(entity)
        map.append(db.get_entity(entity))



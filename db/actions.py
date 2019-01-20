from .database import get_client,get_entity, datastore


def create_action(data):
    ds = get_client()
    key = ds.key('Actions')
    entity = datastore.Entity(
        key=key,
    )
    entity.update(data)
    ds.put(entity)

def update_action(data, id):
    ds = get_client()
    key = ds.key('Actions', int(id))
    entity = datastore.Entity(
        key=key,
        )
    if 'id' in data:
        del data['id']
    entity.update(data)
    ds.put(entity)
    return get_entity(entity)

def get_uncompleted_actions(world, action):
    ds = get_client()
    query = ds.query(kind = 'Player')
    query.add_filter('action', '=', action)
    query.add_filter('world', '=', world)
    query.add_filter('status', '=', 'uncompleted')
    results = []
    for entity in query.fetch():
        results.append(get_entity(entity))
    return results



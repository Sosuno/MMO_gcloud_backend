from .database import get_client,get_entity, datastore
from .timestamps import current_timestamp, current_date


def get_user(username):
    ds = get_client()
    query = ds.query(kind = 'User')
    query.add_filter('username', '=', username)
    result = list(query.fetch())
    
    if result is None:
        return None
    elif not result:
        return None
    r = result.pop()
    return get_entity(r) 

def user_read(id):
    ds = get_client()
    key = ds.key('User', int(id))
    results = ds.get(key)
    return get_entity(results)

def user_update(data, id):
    ds = get_client()
    key = ds.key('User', int(id))
    entity = datastore.Entity(
        key=key,
        )
    if 'id' in data:
        del data['id']
    entity.update(data)
    ds.put(entity)
    return get_entity(entity)

#TODO dodać hashowanie hasla
def user_create(data):
    ds = get_client()
    key = ds.key('User')
    entity = datastore.Entity(
        key=key,
    )
    data['avatarURL'] = 'https://storage.googleapis.com/arc-mmo-game/avatars/avatar-placeholder.png'
    data['created'] = current_date()
    data['loginAttempt'] = 0
    data['status'] = 'active'
    data['access'] = 'normal'
    entity.update(data)
    ds.put(entity)
    return get_entity(entity)
    
def user_delete(id):
    ds = get_client()
    key = ds.key('User', int(id))
    ds.delete(key)

def is_user_in_db(username):
    ds = get_client()
    query = ds.query(kind='User')
    query.add_filter('username', '=', username)
    result = list(query.fetch())
    if result:
        return True
    else:
        return False

def is_correct_user(username, password):
    ds = get_client()
    query = ds.query(kind = 'User')
    query.add_filter('username', '=', username)
    query.add_filter('password', '=', password)
    result = list(query.fetch())
    if result:
        return True
    else:
        return False
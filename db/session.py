from .database import get_client,get_entity, datastore
from .timestamps import current_timestamp
import uuid

def create_session(username):
    ds = get_client()
    key = ds.key('Session')
    entity = datastore.Entity(key=key)
    entity.update({
        'sessionID': str(uuid.uuid1()),
        'user': username,
        'status': 'active'
    })
    ds.put(entity)
    return entity

def destroy_session(uuid):
    ds = get_client()
    query = ds.query(kind = 'Session')
    query.add_filter('sessionID', '=', uuid)
    results = list(query.fetch())
    for result in results:
        r = get_entity(result)
        key = ds.key('Session', int(r['id']))
        ds.delete(key)

def destroy_all_user_sessions(username = None):
    ds = get_client()
    query = ds.query(kind = 'Session')
    if username is not None:
        query.add_filter('user', '=', username)
    results = list(query.fetch())

    for result in results:
        r = get_entity(result)
        key = ds.key('Session', int(r['id']))      
        ds.delete(key)

def check_if_session_active(uuid):
    ds = get_client()
    query = ds.query(kind = 'Session')
    query.add_filter('sessionID', '=', uuid)
    query.add_filter('status', '=', 'active')
    result = list(query.fetch())
    if result is None:
        return False
    elif not result:
        return False
    else:
        return True

def get_username_from_session(uuid):
    ds = get_client() 
    query = ds.query(kind = 'Session')
    query.add_filter('sessionID', '=', uuid)
    result = list(query.fetch())
    if result is None:
        return None
    elif not result:
        return None
    else:
        r = result.pop()
        return r['user']

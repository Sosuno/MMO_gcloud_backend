import timestamps
import database
import uuid

date = timestamps
db = database

def create_session(username):
    ds = db.get_client()

    key = ds.key('Session')
    entity = db.datastore.Entity(key=key)
    entity.update({
        'sessionID': str(uuid.uuid1()),
        'user': username,
        'status': 'active'
    })
    ds.put(entity)
    return entity

def destroy_session(uuid):
    ds = db.get_client()
    query = ds.query(kind = 'Session')
    query.add_filter('sessionID', '=', uuid)
    results = list(query.fetch())
    for result in results:
        r = db.get_entity(result)
        key = ds.key('Session', int(r['id']))
        ds.delete(key)

def destroy_all_user_sessions(username):
    ds = db.get_client()
    query = ds.query(kind = 'Session')
    query.add_filter('user', '=', username)
    results = list(query.fetch())

    for result in results:
        r = db.get_entity(result)
        key = ds.key('Session', int(r['id']))      
        ds.delete(key)

def check_if_session_active(uuid):
    ds = db.get_client()
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
    ds = db.get_client() 
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

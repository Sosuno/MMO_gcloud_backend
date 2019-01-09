import database
import timestamps

time = timestamps
db = database

def get_user(username):
    ds = db.get_client()
    query = ds.query(kind = 'User')
    query.add_filter('username', '=', username)
    result = list(query.fetch())
    
    if result is None:
        return None
    elif not result:
        return None
    r = result.pop()
    return db.get_entity(r) 

def user_read(id):
    ds = db.get_client()
    key = ds.key('User', int(id))
    results = ds.get(key)
    return db.get_entity(results)

def user_update(data, id):
    ds = db.get_client()
    key = ds.key('User', int(id))
    entity = db.datastore.Entity(
        key=key,
        )
    if 'id' in data:
        del data['id']
    entity.update(data)
    ds.put(entity)
    return db.get_entity(entity)

#TODO dodać hashowanie hasla
def user_create(data):
    ds = db.get_client()
    key = ds.key('User')
    entity = db.datastore.Entity(
        key=key,
    )
    data['avatarURL'] = 'https://storage.googleapis.com/arc-mmo-game/avatars/avatar-placeholder.png'
    data['created'] = time.current_date()
    data['loginAttempt'] = 0
    data['status'] = 'active'
    data['access'] = 'normal'
    entity.update(data)
    ds.put(entity)
    return db.get_entity(entity)
    
def user_delete(id):
    ds = db.get_client()
    key = ds.key('User', int(id))
    ds.delete(key)

def is_user_in_db(username):
    ds = db.get_client()
    query = ds.query(kind='User')
    query.add_filter('username', '=', username)
    result = list(query.fetch())
    if result:
        return True
    else:
        return False

def is_correct_user(username, password):
    ds = db.get_client()
    query = ds.query(kind = 'User')
    query.add_filter('username', '=', username)
    query.add_filter('password', '=', password)
    result = list(query.fetch())
    if result:
        return True
    else:
        return False
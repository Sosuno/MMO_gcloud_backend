from .database import get_client,get_entity, datastore
from .timestamps import current_timestamp


def create_login_log(username):
    ds = get_client()
    key = ds.key('Logs')
    entity = datastore.Entity(key=key)
    entity.update({
        'user': username,
        'login time': current_timestamp()
    })
    entity.update()
    ds.put(entity)


def get_login_logs():
    ds = get_client()
    query = ds.query(kind = 'Logs')
    results = list(query.fetch())
    return results


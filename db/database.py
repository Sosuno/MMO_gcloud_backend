from google.cloud import datastore

builtin_list = list

def init_app(app):
    pass

def get_client():
    return datastore.Client('solwit-pjatk-arc-2018-gr4')

def get_entity(entity):
    if not entity:
        return None
    if isinstance(entity, builtin_list):
        entity = entity.pop()

    entity['id'] = entity.key.id
    return entity

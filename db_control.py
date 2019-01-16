from db import buildings, players, user, worldMap, worlds, timestamps, session, database

def login(data = None):
    
    if data is None:
        return False
    if user.is_correct_user(data['login'], data['password']):
            session.destroy_all_user_sessions(data['login'])
            my_session = session.create_session(data['login'])
            return my_session['sessionID']
    else:
        return False

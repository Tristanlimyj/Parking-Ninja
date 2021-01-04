from bot import db
from bot.model import UserInfo, UserSetting

def current_user(user_id):
    current_user = UserInfo.query.filter_by(
        user_id=str(user_id)
    ).first()

    return current_user

def add_user(sender_info):
    from_keys = sender_info.keys()
    
    # Initializing the variables
    first_name, username, last_name = '', '', ''
    user_id = sender_info['id']
        
    # Since these options are optional need to check
    if 'first_name' in from_keys: first_name = sender_info['first_name']
    if 'username' in from_keys: username = sender_info['username']
    if 'last_name' in from_keys: last_name = sender_info['last_name']
        
    new_user = UserInfo(user_id, username, first_name, last_name)
    db.session.add(new_user)
    db.session.commit()
    new_user_settings = UserSetting(new_user.id)
    db.session.add(new_user_settings)
    db.session.commit()
    return new_user


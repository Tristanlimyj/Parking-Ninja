from bot import db
from bot.model import UserMessage, UserSystemResponse
    
def log_message(main_table_id, update_id, body_key, message):
    new_message = UserMessage(
        main_table_id, 
        update_id, 
        body_key,
        message
    )
    db.session.add(new_message)
    db.session.commit()

    return new_message

def create_log_response(message_id, message_type, user_id):
    new_response = UserSystemResponse(
        message_id, 
        message_type,
        user_id
    )
    
    db.session.add(new_response)
    db.session.commit()

    return new_response

def complete_log_response(message_id, response_text, server_response_body, response_msg_id):
    UserResponse = UserSystemResponse.query.filter_by(user_message_id=message_id).first()
    UserResponse.message_body = response_text
    UserResponse.response_server = server_response_body
    UserResponse.reponse_message_id = response_msg_id
    db.session.add(UserResponse)
    db.session.commit()

    return UserResponse
def get_message_body_key(message):
    message_body_key = list(message.keys())[1]
    message_body = message[message_body_key]

    return message_body, message_body_key
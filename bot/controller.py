from bot import db
from flask import Blueprint, request, make_response
from bot.model import UserInfo, UserMessage
from .Modules import CleanInputFunc, UserFunc, LoggingFunc
from bot.Modules.Bot import Bot

tele_blueprint = Blueprint(
    'tele', __name__
)

@tele_blueprint.route('/', methods=['POST'])
def index():
    # Getting the User Input
    message =  request.json
    # Getting the Key of the Body and Body
    message_body, message_body_key = CleanInputFunc.get_message_body_key(message)
    # Checking if the user has used this service before
    current_user = UserFunc.current_user(message_body['from']['id'])
    # if first time add them in to the DB
    if current_user == None:
        current_user = UserFunc.add_user(message_body['from'])

    # Add the Message into the Log
    new_message = LoggingFunc.log_message(
        current_user.id,
        message['update_id'],
        message_body_key,
        message
    )

    # Creating the Bot Object
    bot = Bot(current_user, new_message)
    # Getting the type
    if 'text' in message_body.keys():
        bot.text_action(message_body['text'])
    elif 'location' in message_body.keys():
        bot.location_action(message_body['location'])
    elif 'data' in message_body.keys():
        bot.inline_keyboard_action(message_body['data'])
    else:
        print(message_body)
        raise Exception('New datatype')

    return make_response(('Success',200))

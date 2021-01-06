import requests, json, os
from bot.Modules import LoggingFunc
from bot.model import UserSetting

base_url = 'https://api.telegram.org/bot' + os.getenv('TOKEN')

def send_message(url, params, response_text,message_id):
    # Getting the Response from the Server
    res = requests.post(url , params=params)
    response_body = json.loads(res.text)

    try:
        LoggingFunc.complete_log_response(
            message_id, 
            response_text,
            response_body,
            response_body['result']['message_id']
        )
    except:
        send_message(
            url,
            params, 
            'There has been an error please send your location again!',
            message_id
        )
    return True

def create_edit_msg_params(api_end_point, chat_id, previous_message_id ,text, reply_markup):
    url = base_url + api_end_point
    params = {
        'chat_id': chat_id,
        'message_id' : previous_message_id,
        'text': text,
        'parse_mode': 'Markdown',
        'reply_markup' : json.dumps(reply_markup),
    }

    return url, params

def create_new_msg_params(api_end_point, chat_id, message, reply_markup):
    url = base_url + api_end_point
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown',
        'reply_markup' : json.dumps(reply_markup),
    }

    return url, params
# The buttons will come in as a list of values
def create_inline_keyboard(btn_list):
    inline_keyboard = {
        'inline_keyboard' : btn_list
    }

    return inline_keyboard

def create_reply_keyboard(allowed_responses):
    button_set = list(map(lambda btn: [btn] if type(btn) == str else btn, allowed_responses))

    button_set.append(create_send_location_btn())
    keyboard = {
        'keyboard' : button_set,
        'rezise_keyboard' : True,
        'one_time_keyboard' : False,
    }

    return keyboard

def create_send_location_btn():
    send_location = {
        'text' :  'Send Location📍',
        'request_location': True
    }

    return [send_location]
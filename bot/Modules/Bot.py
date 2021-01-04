from bot import db
from bot.Modules import GoogleFunc, LocationActions, StaticActions, LoggingFunc, TeleFunc, InlineBtnFunc
from bot.model import UserSystemResponse
from sqlalchemy import func
import os, re

base_url = 'https://api.telegram.org/bot'

class Bot():
    def __init__(self, user, message):
        self.url = base_url + os.getenv('TOKEN')
        self.user = user
        self.message = message

    '''
        Evaluate the response into 3 main cats
        1. Location Send
        2. Settings Tab
        3. Text
    '''

    '''
        For location
        Query the db for the nearest few carparks and their availablilty
        if there no nearby carpark inform them 
    '''
    def location_action(self, user_input):
        LoggingFunc.create_log_response(self.message.id, 'location', self.user.id)
        
        # Getting User Input
        user_settings = self.user.setting[0]
        user_location = (user_input['latitude'], user_input['longitude'])
        
        # Getting all the of the users vehicle type
        carpark_coordinates = LocationActions.user_vehicle_type_all_lots(user_settings)
        
        # Getting the nearby parking lots within the specified range
        inline_btn_list, nearby_carpark_list =  LocationActions.getting_nearby_carpark(carpark_coordinates,user_location, user_settings.search_distance_km)
        
        if nearby_carpark_list:
            response_text = LocationActions.nearby_carpark_message(nearby_carpark_list)
            # Creating Reply Params
            parking_option_btn = InlineBtnFunc.create_parking_option_btn(inline_btn_list, user_settings.vehicle_type)
            reply_markup = TeleFunc.create_inline_keyboard(parking_option_btn)
            url, params = TeleFunc.create_new_msg_params('/sendMessage', self.user.user_id, response_text, reply_markup)
                
            TeleFunc.send_message(url, params, response_text,self.message.id)
        else:
            btn_list, response_text = StaticActions.no_nearby_carpark()
            self.send_message_reply_kb(btn_list, response_text)

    def inline_keyboard_action(self, user_input):
        previous_message = self.previous_message()
        LoggingFunc.create_log_response(self.message.id, 'location', self.user.id)
        '''
            All Inline Btns have 2 kinds of input 
            1) The value to query
            2) The action which that need to take place
        '''
        item_id, action = user_input.split('---')
        
        if action == 'BACK':
            target_message = UserSystemResponse.query.filter_by(id=int(item_id)).first()
            previous_message = target_message
            response_text = target_message.response_server['result']['text']
            reply_markup = target_message.response_server['result']['reply_markup']
        else:
            selected_carpark = LocationActions.get_searched_lot(action, item_id)

            indv_carpark_dict = LocationActions.current_parking_info(selected_carpark)
            response_text = LocationActions.individual_carpark_info_text(selected_carpark.pp_name,indv_carpark_dict)
            # Creating the Btns for the result
            google_link = GoogleFunc.create_google_link(selected_carpark)

            google_link_btn = InlineBtnFunc.create_google_link_btn(google_link)
            back_btn = InlineBtnFunc.create_back_btn(previous_message.id)

            reply_markup = TeleFunc.create_inline_keyboard([google_link_btn,back_btn])

        # Need to create params for a update message
        url, params = TeleFunc.create_edit_msg_params(
                '/editMessageText', 
                self.user.user_id,
                previous_message.reponse_message_id,
                response_text,
                reply_markup
            )

        # Edit
        TeleFunc.send_message(url, params, response_text, self.message.id)
    
    def text_action(self,user_input):
        # Logging the Response
        LoggingFunc.create_log_response(self.message.id, user_input, self.user.id)
        # Getting User input
        user_input = user_input.lower().replace('/', '')

        if re.search('---settings$', user_input):
            self.setting_action(user_input)
        else:
            self.static_actions(user_input)

    # For the user to edit his settings
    def setting_action(self, user_input):  
        item_id, action = user_input.split('---')

        user_setting = self.user.setting
        user_setting.vehicle_type = item_id.upper()

        btn_list, response_text = StaticActions.change_setting(item_id)

        self.send_message_reply_kb(btn_list, response_text)
    
    # For all predefined actions
    def static_actions(self, user_input):
        try:
            # Get the right action based on input
            action = StaticActions.get_action(user_input)
            btn_list, response_text = action()
            self.send_message_reply_kb(btn_list, response_text)
        except:
            self.send_error_message

    '''
        These are supporting Functions which will not
        be referenced outside of this class. And used
        to support the main functions.
    '''
    # This is to send messages using reply keyboards
    def send_message_reply_kb(self, btn_list, response_text):
        reply_markup = TeleFunc.create_reply_keyboard(btn_list)
        url, params = TeleFunc.create_new_msg_params('/sendMessage', self.user.user_id, response_text, reply_markup)
        TeleFunc.send_message(url, params, response_text, self.message.id)

    # To send an error message in the event that there is a error
    def send_error_message(self):
        btn_list, response_text = StaticActions.error()
        self.send_message(btn_list, response_text)
    
    # To get the previous Message
    def previous_message(self):
        '''
            Using the user id query the User response
            Get the latest response Message
            Return ID
        '''
        previous_messsage_id = db.session.query(func.max(UserSystemResponse.id)).filter(UserSystemResponse.user_id==self.user.id).first()
        previous_message = UserSystemResponse.query.filter_by(id=previous_messsage_id).first()
        return previous_message


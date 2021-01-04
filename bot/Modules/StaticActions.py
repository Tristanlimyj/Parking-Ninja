from bot.Modules import TeleFunc, StaticActions

def get_action(user_input):
    options = {
                    'start' : StaticActions.start,
                    'description' : StaticActions.description,
                    'settings ⚙️' : StaticActions.settings,
    }
    
    return options[user_input]
    
def start():
    text = 'Welcome to the Parking Ninja Bot☺️'
    btn_list = [['Settings ⚙️','Start','Description']]

    return btn_list, text

def description():
    text = 'Hihi!\n\n'
    text += 'This bot is created to enable people to be able to find nearby parking lots!\n\n'
    text += 'All the data provided is from the URA Dataset\n\n'

    btn_list = [['Settings ⚙️','Start','Description']]
    
    return btn_list, text

def change_setting(vehicle_type):
    text = 'We will now be searching for {} lots.'.format(vehicle_type)
    btn_list = [['Settings ⚙️','Start','Description']]
    
    return btn_list, text

def settings():
    text = 'Hihi!\n\n'
    text += 'The Default vehicle will be a car! '
    text += 'Use the buttons bellow to change the vehicle type you would like to search for.'
    btn_list = [['Car---settings'], ['Motorcycle---settings'], ['Heavy Vehicle---settings']]
    
    return btn_list, text

def no_nearby_carpark():
    text = 'There are no carparks within 500m of your location!'
    btn_list = [['Settings ⚙️','Start','Description']]
    
    return btn_list, text

def error():
    text = 'Sorry! I do not understand what you are saying😞'
    btn_list = [['Settings ⚙️','Start','Description']]
    
    return btn_list, text

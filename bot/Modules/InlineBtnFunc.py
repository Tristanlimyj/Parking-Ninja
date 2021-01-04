def create_back_btn(previous_message_id):
    back_btn = {
        'text' : 'Back',
        'callback_data' : '{}---BACK'.format(previous_message_id),
    }

    return [back_btn]

def create_google_link_btn(google_link):
    back_btn = {
        'text' : 'Google Maps Link',
        'url' : google_link,
    }

    return [back_btn]

def create_parking_option_btn(btn_list,vehicle_type):
    completed_btn_list = []
    
    for btn in btn_list:
        btn_details =  {
            'text' : btn['text'],
            'callback_data' : '{}---{}'.format(btn['callback_data'], vehicle_type),
        }
        completed_btn_list.append([btn_details])

    return completed_btn_list
import pytz
from datetime import datetime

def current_date():
    tz = pytz.timezone('Asia/Singapore')
    current_date = datetime.now(tz).strftime("%d/%m/%Y")
    
    return current_date

def convert_to_24H_clock(time):
    return_time, AMPM  = time.split(' ', 1)
    return_time = return_time.replace('.', '')
    if AMPM.upper() == 'PM': return_time = int(return_time) + 1200

    return str(int(return_time))
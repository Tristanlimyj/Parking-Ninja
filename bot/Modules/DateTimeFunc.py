import pytz
import datetime
def current_day_of_week():
    tz = current_timezone()
    day = datetime.datetime.today().replace(tzinfo=tz).weekday()
    return int(day)

def current_time():
    tz = current_timezone()
    datetime_obj = datetime.datetime.now().replace(tzinfo=tz)
    time_string = datetime_obj.strftime("%H%M")

    return int(time_string)

def current_timezone():
     return pytz.timezone('Asia/Singapore')

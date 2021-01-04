from dotenv import load_dotenv
import requests, os, json
from . import DatabaseFunc, DateFunc

load_dotenv()
access_key = os.getenv("ACCESSKEY")

# Requst Requiring the token only
def ak_request(url):
    headers = { 
        "AccessKey" : access_key,
    }

    res = requests.post(url, headers=headers)
    response_body = json.loads(res.text)

    return response_body

# Requst that requir both the token and access key
def tk_ak_request(url, token):
    headers = {
        "AccessKey" : access_key,
        "Token" : token,
    }

    res = requests.post(url, headers=headers)
    response_body = json.loads(res.text)
    
    return response_body

# Getting the Token for today
def get_todays_token():
    current_date = DateFunc.current_date()
    try:
        Connection = DatabaseFunc.connecting_to_db('parking_ninja')
        cur = Connection.cursor()

        # Getting the Daily Token
        cur.execute(
        '''
            SELECT token FROM daily_token
            WHERE date = %s;
        ''',
            (current_date,)
        )

        data =  cur.fetchall()[0]
        return data[0]
    except:
        Connection.close()
        return False
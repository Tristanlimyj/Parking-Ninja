from dotenv import load_dotenv
from db_scripts.DatabaseFunc import DataBaseMethods
import requests
import os, json, pytz
from datetime import datetime

load_dotenv()
access_key = os.getenv("ACCESSKEY")

# Post Response
res = requests.post('https://www.ura.gov.sg/uraDataService/insertNewToken.action', headers={"AccessKey" : access_key})
response_body = json.loads(res.text)

if response_body["Status"] == 'Success':
    Connection = DataBaseMethods.connecting_to_db('parking_ninja')
    cur = Connection.cursor()
    
    tz = pytz.timezone('Asia/Singapore')
    current_date = datetime.now(tz).strftime("%d/%m/%Y")
    cur.execute(
        """
            INSERT INTO daily_token (date, token)
            Values (%s, %s)
        """
        ,
            (current_date,response_body['Result'])
    )
    Connection.commit()
    Connection.close()


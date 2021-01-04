from CommonFunc import DatabaseFunc, DateFunc, RequestFunc

# Geting the Token
response_body = RequestFunc.ak_request('https://www.ura.gov.sg/uraDataService/insertNewToken.action')

if response_body["Status"] == 'Success':
    Connection = DatabaseFunc.connecting_to_db('parking_ninja')
    cur = Connection.cursor()
    
    current_date = DateFunc.current_date()

    cur.execute(
        """
            INSERT INTO daily_token (date, token)
            Values (%s, %s)
        """
    ,
        (current_date, response_body['Result'])
    )
    Connection.commit()
    Connection.close()


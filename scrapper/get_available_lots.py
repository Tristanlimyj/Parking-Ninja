from psycopg2 import sql
from CommonFunc import DatabaseFunc, DateFunc, RequestFunc, TableInfo

try:
    Connection = DatabaseFunc.connecting_to_db('parking_ninja')
    cur = Connection.cursor()

    available_lots = RequestFunc.tk_ak_request(
            'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Availability',
            RequestFunc.get_todays_token()
        )
    # When Refreshing I will be dropping the previous tables
    # This is to prevent duplicates

    tables = TableInfo.type_table('available_lot')
    for table in tables:
        DatabaseFunc.clear_table_data(table)

    # Populating the new tables with the new results
    for indv_lot in available_lots["Result"]:
        target_table = TableInfo.table_type(indv_lot['lotType'].upper())
        # Retreiving the ID in the main table
        cur.execute(
            sql.SQL(
                '''
                    SELECT * from {}
                    WHERE pp_code=%s;
                '''
            )
            .format(
                sql.Identifier(target_table['main_table'])
            )
            , 
                (indv_lot['carparkNo'],)
        )
        result_of_query = cur.fetchone()
        miss_counter = 0
        if result_of_query != None:
            # Inserting the Available Lots into the DB
            cur.execute(
                    sql.SQL(
                        '''
                            INSERT INTO {} (
                                main_table_id,
                                lots_available
                            )
                            VALUES (%s,%s);
                        '''
                    )
                    .format(sql.Identifier(target_table['available_lot']))
                    ,
                    (result_of_query[0], indv_lot['lotsAvailable'])
                )

    Connection.commit()
    Connection.close() 
    print('-'*100)
    print('Completed without Errors')

except Exception as e:
    Connection.close()
    raise Exception(e)
    
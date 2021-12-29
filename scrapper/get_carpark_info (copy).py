from psycopg2 import sql
from CommonFunc import DatabaseFunc, DateFunc, RequestFunc, TableInfo
from CommonFunc.SVY21Converter import SVY21

try:
    Connection = DatabaseFunc.connecting_to_db('parking_ninja')
    cur = Connection.cursor()

    '''
        When Refreshing I will be dropping the previous tables
        This is to prevent duplicates
        Note:
        The reason why i dont just delete from the main table 
        and let it casade is cause for some reason it only
        works when i use sql aclhemy and not using raw sql
    '''
    table_list = [
        'carpark_geometry', 
        'carpark_info', 
        'available_lot', 
        'main_table'
    ]

    for type_table in table_list:
        tables = TableInfo.type_table(type_table)
        for table in tables:
            DatabaseFunc.clear_table_data(table)

    lot_info = RequestFunc.tk_ak_request(
            'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details',
            RequestFunc.get_todays_token()
        )

    # Adding Info into DB
    for indv_lot in lot_info["Result"]:
        remarks = indv_lot['remarks'] if 'remarks' in indv_lot.keys() else ''

        # Filtering the Data into it's input
        target_table = TableInfo.table_type(indv_lot['vehCat'].upper())
        
        # Check if there is an entry with the same pp_code
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
                (indv_lot['ppCode'],)
        )
        result_of_query = cur.fetchone()
        row_id = ''
        # There has been no prior input 
        if result_of_query == None:
            # Inserting into the Main Table
            cur.execute(
                sql.SQL(
                    '''
                        INSERT INTO {} (
                            pp_code,
                            pp_name
                        )
                        VALUES (%s,%s)
                        RETURNING id;
                    '''
                )
                .format(sql.Identifier(target_table['main_table']))
                ,
                (indv_lot['ppCode'],indv_lot['ppName'],)
            )
            
            row_id = cur.fetchone()[0]

            cur.execute(
                sql.SQL(
                    '''
                        INSERT INTO {} (
                            main_table_id,
                            start_time,
                            end_time,
                            weekday_rate,
                            weekday_min,
                            satday_rate,
                            satday_min,
                            sun_ph_rate,
                            sun_ph_min,
                            parking_system,
                            park_capacity,
                            remarks
                        )
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        RETURNING id;
                    '''
                )
                .format(sql.Identifier(target_table['carpark_info']))
                ,
                (
                    row_id,
                    DateFunc.convert_to_24H_clock(indv_lot['startTime']),
                    DateFunc.convert_to_24H_clock(indv_lot['endTime']),
                    indv_lot['weekdayRate'],
                    indv_lot['weekdayMin'],
                    indv_lot['satdayRate'],
                    indv_lot['satdayMin'],
                    indv_lot['sunPHRate'],
                    indv_lot['sunPHMin'],
                    indv_lot['parkingSystem'],
                    indv_lot['parkCapacity'],
                    remarks
                )
            )
            

        if result_of_query: row_id = result_of_query[0]
        
        # Check if the coordinates already exist
        if 'geometries' in indv_lot.keys():
            for coordinates in indv_lot['geometries']:
                cur.execute(
                    sql.SQL(
                        '''
                            SELECT * FROM {}
                            WHERE svy21_coordinates=%s AND
                            main_table_id=%s;
                        '''
                    )
                    .format(sql.Identifier(target_table['carpark_geometry']))
                    ,
                    (coordinates['coordinates'],row_id)
                )

                coordinate_row = cur.fetchone()

                if coordinate_row == None:
                    # Convert from SVY21 to Log Lat
                    converter = SVY21()
                    east, north = coordinates['coordinates'].split(',')
                    lat, lon =  converter.computeLatLon(float(north), float(east))
                    cur.execute(
                        sql.SQL(
                            '''
                                INSERT INTO {} (
                                    main_table_id,
                                    svy21_coordinates,
                                    easting,
                                    northing
                                )
                                VALUES (%s,%s,%s,%s);
                            '''
                        )
                        .format(sql.Identifier(target_table['carpark_geometry']))
                        ,
                        (
                            row_id,
                            coordinates['coordinates'],
                            lat,
                            lon
                        )
                    )

    Connection.commit()
    Connection.close() 
    print('-'*100)
    print('Completed without Errors')

except Exception as e:
    print(e)
    Connection.close()
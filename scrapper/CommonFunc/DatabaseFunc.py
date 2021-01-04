import psycopg2
from psycopg2 import sql 

def connecting_to_db(DBName=''):
    DB_setting = 'dbname={}'.format(DBName) if DBName else '' 
    con = psycopg2.connect("host=localhost {} user=tristan".format(DB_setting))
    return con

def drop_db(DBName=''):
    Connection = connecting_to_db()
    try:
        cur = Connection.cursor()
        cur.execute(
            sql.SQL(
                '''
                    DROP DATABASE {};
                '''
                .format(sql.Identifier(DBName))
            )
        )
        Connection.commit()
        Connection.close()
    except:
        Connection.close()

def clear_table_data(table):
    Connection = connecting_to_db('parking_ninja')
    try:
        cur = Connection.cursor()

        cur.execute(
            sql.SQL(
                '''
                    DELETE FROM {};
                '''
            ).format(sql.Identifier(table))
        )
        Connection.commit()
        Connection.close()

    except Exception as e:
        Connection.close()
        raise Exception(e)


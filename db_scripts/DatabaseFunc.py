import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 

class DataBaseMethods():
    def connecting_to_db(DBName=''):
        DB_setting = 'dbname={}'.format(DBName) if DBName else '' 
        con = psycopg2.connect("host=localhost {} user=tristan".format(DB_setting))
        return con

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 
from DatabaseFunc import DataBaseMethods

connection = DataBaseMethods.connecting_to_db()

connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cursor = connection.cursor()
cursor.execute(""" DROP DATABASE parking_ninja; """)

connection.close()
print(connection)
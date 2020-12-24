import psycopg2
from DatabaseFunc import DataBaseMethods

connection = DataBaseMethods.connecting_to_db('parking_ninja')
cursor = connection.cursor()

# Table Storing the Daily Token
cursor.execute(
    """ 
        CREATE TABLE daily_token (
            id SERIAL PRIMARY KEY,
            date date, 
            token varchar(200)
        )
    """
)

connection.commit()
connection.close()

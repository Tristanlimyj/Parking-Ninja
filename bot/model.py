from bot import db
from sqlalchemy.dialects.postgresql import JSON

'''
    The model can be split into 3 main parts
    1. The Parking lot data that will be furthur
    split into 3 main categories. 
    2. All the user related input and information
    3. Webscrapping related tables.
'''
'''
    Parking Lot Data Section 
    All the Parking Lot data will be split into 3 categories
    1. MotorCycle
    2. Cars
    3. Heavy Vehicles
    
    This also acts as a Partition Making it Cost less per query

    For each category there will be 1 parent table and 3 children table
    which will be linked via the PK in the main table.

'''
# Car Related Tables
class CarCarparkMainTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pp_code = db.Column(db.String(20))
    pp_name = db.Column(db.String(124))
    carpark_info = db.relationship(
        'CarCarparkInfo', 
        backref='main_table', 
        cascade="all, delete",
        lazy=True
    )
    carpark_geometry = db.relationship(
        'CarCarparkGeometry', 
        backref='main_table', 
        cascade="all, delete",
        lazy=True
    )
    carpark_available_lot = db.relationship(
        'CarAvailableLot', 
        backref='main_table', 
        cascade="all, delete",
        lazy=True
    )

class CarCarparkInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_table_id = db.Column(db.Integer, db.ForeignKey('car_carpark_main_table.id'), nullable=False)
    start_time = db.Column(db.Integer)
    end_time = db.Column(db.Integer)
    weekday_rate = db.Column(db.String(20))
    weekday_min = db.Column(db.String(20))
    satday_rate = db.Column(db.String(20))
    satday_min = db.Column(db.String(20))
    sun_ph_rate = db.Column(db.String(20))
    sun_ph_min = db.Column(db.String(20))
    parking_system = db.Column(db.String(20))
    park_capacity = db.Column(db.Integer())
    remarks = db.Column(db.String(124))

class CarCarparkGeometry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_table_id = db.Column(db.Integer, db.ForeignKey('car_carpark_main_table.id'), nullable=False)
    svy21_coordinates = db.Column(db.String(50))
    northing = db.Column(db.String(50))
    easting = db.Column(db.String(50))

class CarAvailableLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_table_id = db.Column(db.Integer, db.ForeignKey('car_carpark_main_table.id'), nullable=False)
    lots_available = db.Column(db.Integer)

# MotorBike Related Tables
class MotorBikeCarparkMainTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pp_code = db.Column(db.String(20))
    pp_name = db.Column(db.String(124))
    carpark_info = db.relationship('MotorBikeCarparkInfo', backref='main_table', lazy=True)
    carpark_geometry = db.relationship('MotorBikeCarparkGeometry', backref='main_table', lazy=True)
    carpark_available_lot = db.relationship('MotorBikeAvailableLot', backref='main_table', lazy=True)

class MotorBikeCarparkInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_table_id = db.Column(db.Integer, db.ForeignKey('motor_bike_carpark_main_table.id'), nullable=False)
    start_time = db.Column(db.Integer)
    end_time = db.Column(db.Integer)
    weekday_rate = db.Column(db.String(20))
    weekday_min = db.Column(db.String(20))
    satday_rate = db.Column(db.String(20))
    satday_min = db.Column(db.String(20))
    sun_ph_rate = db.Column(db.String(20))
    sun_ph_min = db.Column(db.String(20))
    parking_system = db.Column(db.String(20))
    park_capacity = db.Column(db.Integer())
    remarks = db.Column(db.String(124))

class MotorBikeCarparkGeometry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_table_id = db.Column(db.Integer, db.ForeignKey('motor_bike_carpark_main_table.id'), nullable=False)
    svy21_coordinates = db.Column(db.String(50))
    northing = db.Column(db.String(50))
    easting = db.Column(db.String(50))

class MotorBikeAvailableLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_table_id = db.Column(db.Integer, db.ForeignKey('motor_bike_carpark_main_table.id'), nullable=False)
    lots_available = db.Column(db.Integer)

# Heavy Vehicles Related Tables
class HeavyVehicleCarparkMainTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pp_code = db.Column(db.String(20))
    pp_name = db.Column(db.String(124))
    carpark_info = db.relationship('HeavyVehicleCarparkInfo', backref='main_table', lazy=True)
    carpark_geometry = db.relationship('HeavyVehicleCarparkGeometry', backref='main_table', lazy=True)

class HeavyVehicleCarparkInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_table_id = db.Column(db.Integer, db.ForeignKey('heavy_vehicle_carpark_main_table.id'), nullable=False)
    start_time = db.Column(db.Integer)
    end_time = db.Column(db.Integer)
    weekday_rate = db.Column(db.String(20))
    weekday_min = db.Column(db.String(20))
    satday_rate = db.Column(db.String(20))
    satday_min = db.Column(db.String(20))
    sun_ph_rate = db.Column(db.String(20))
    sun_ph_min = db.Column(db.String(20))
    parking_system = db.Column(db.String(20))
    park_capacity = db.Column(db.Integer())
    remarks = db.Column(db.String(124))

class HeavyVehicleCarparkGeometry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_table_id = db.Column(db.Integer, db.ForeignKey('heavy_vehicle_carpark_main_table.id'), nullable=False)
    svy21_coordinates = db.Column(db.String(50))
    northing = db.Column(db.String(50))
    easting = db.Column(db.String(50))

class HeavyVehicleAvailableLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_table_id = db.Column(db.Integer, db.ForeignKey('heavy_vehicle_carpark_main_table.id'), nullable=False)
    lots_available = db.Column(db.Integer)

'''
    User Related Section
    There will be 4 tables in this section
    3 tables will be linked like a chain
    In Order of Importance
    1. User Information
    2. User Message
    3. System Response

    The 4th Table will be used to store the user's settings

    The reason for storing the user message and system response
    is the hope of being able to use the data to use tensorflow
    in the future to make the bot smart and 'teach' it the 
    appropriate response
'''
class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50))
    username = db.Column(db.String(124))
    first_name = db.Column(db.String(124))
    last_name = db.Column(db.String(124))
    messages = db.relationship(
        'UserMessage',
        backref='user_info',
        lazy=True,
        cascade="all, delete"
    )
    response = db.relationship(
        'UserSystemResponse', 
        backref='user_info',
        lazy=True,
        cascade="all, delete"
    )
    
    setting = db.relationship(
        'UserSetting',
        backref='user_info',
        lazy=True,
        cascade="all, delete"
    )

    def __init__(self, user_id, username, first_name, last_name):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

class UserSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_type = db.Column(db.String(50))
    search_distance_km = db.Column(db.Float)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user_info.id'),
        nullable=False
    )

    def __init__(self, user_id):
        self.user_id = user_id
        self.vehicle_type = 'CAR'
        self.search_distance_km = 0.5


class UserMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), nullable=False)
    update_id = db.Column(db.Integer)
    message_type = db.Column(db.String(50))
    message_body = db.Column(JSON)
    response = db.relationship(
        'UserSystemResponse', 
        backref='user_message',
        lazy=True,
        cascade="all, delete"
    )

    def __init__(self,user_id, update_id, message_type, message_body):
        self.user_id = user_id
        self.update_id = update_id
        self.message_type = message_type
        self.message_body = message_body

class UserSystemResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message_id = db.Column(db.Integer ,db.ForeignKey('user_message.id'), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user_info.id')
    )
    message_type = db.Column(db.String(50))
    message_body = db.Column(db.String)
    response_server = db.Column(JSON)
    reponse_message_id = db.Column(db.Integer)

    def __init__(self,user_message_id, message_type, user_id):
        self.user_message_id = user_message_id
        self.message_type = message_type
        self.user_id = user_id

'''
    WebScrapping Related Table
    There is 1 Table in this section which is the to store the
    daily token given by URA
'''
class DailyToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    token = db.Column(db.String(200))

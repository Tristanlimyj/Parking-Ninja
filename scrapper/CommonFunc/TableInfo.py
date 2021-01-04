def CategoryTable(category):
    tables = {
        'C' : {
            "available_lot": "car_available_lot",
            "carpark_geometry": "car_carpark_geometry",
            "carpark_info": "car_carpark_info",
            "main_table": "car_carpark_main_table",
        },
        'M' : {
            "available_lot": "motor_bike_available_lot",
            "carpark_geometry": "motor_bike_carpark_geometry",
            "carpark_info": "motor_bike_carpark_info",
            "main_table": "motor_bike_carpark_main_table",
        },
        'HV' : {
            "available_lot": "heavy_vehicle_available_lot",
            "carpark_geometry": "heavy_vehicle_carpark_geometry",
            "carpark_info": "heavy_vehicle_carpark_info",
            "main_table": "heavy_vehicle_carpark_main_table",
        },
    }
    return tables[category]

def table_type(vehCat):
    if vehCat == 'C' or vehCat == 'CAR':
        return CategoryTable('C')
    elif vehCat == 'H' or vehCat == 'HEAVY VEHICLE':
        return CategoryTable('HV')
    elif vehCat == 'M' or vehCat == 'MOTORCYCLE':
        return CategoryTable('M')
    else:
        raise Exception("There is a new type that I have not seen")

def type_table(table_type):
    tables = {
        'available_lot' : [
            'car_available_lot',
            'motor_bike_available_lot',
            'heavy_vehicle_available_lot',
        ],
        'carpark_geometry' : [
            'car_carpark_geometry',
            'motor_bike_carpark_geometry',
            'heavy_vehicle_carpark_geometry',
        ],
        'carpark_info' : [
            'car_carpark_info',
            'motor_bike_carpark_info',
            'heavy_vehicle_carpark_info',
        ],
        'main_table' : [
            'car_carpark_main_table',
            'motor_bike_carpark_main_table',
            'heavy_vehicle_carpark_main_table',
        ] 
    }

    return tables[table_type]
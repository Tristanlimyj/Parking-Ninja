from bot.model import UserSetting, CarCarparkMainTable, MotorBikeCarparkMainTable, HeavyVehicleCarparkMainTable, CarCarparkGeometry, MotorBikeCarparkGeometry, HeavyVehicleCarparkGeometry
from bot.Modules import DateTimeFunc 
import geopy.distance

def user_vehicle_type_all_lots(user_settings):
    if user_settings.vehicle_type == 'CAR':
        carpark_coordinates =  CarCarparkGeometry.query.all()
    elif user_settings.vehicle_type == 'HEAVY VEHICLE':
        carpark_coordinates =  HeavyVehicleCarparkGeometry.query.all()
    else:
         carpark_coordinates =  MotorBikeCarparkGeometry.query.all()
    return carpark_coordinates

def get_searched_lot(category, item_id):
    if category == 'CAR':
        selected_carpark =  CarCarparkMainTable.query.filter_by(pp_code=item_id).first()
    elif category == 'HEAVY VEHICLE':
        selected_carpark =  HeavyVehicleCarparkMainTable.query.filter_by(pp_code=item_id).first()
    else:
        selected_carpark =  MotorBikeCarparkMainTable.query.filter_by(pp_code=item_id).first()
    return selected_carpark

def getting_nearby_carpark(carpark_coordinates, user_location, user_search_distance):
    nearby_carpark_list = []

    for carpark in carpark_coordinates:
        coordinates = (carpark.easting,carpark.northing)
        distance = geopy.distance.distance(coordinates, user_location).km
        if distance <= user_search_distance:
            # If there are no available lots it will check for the
            parking_details = {
                'carpark' : carpark.main_table,
                'distance' : '{}'.format(distance),
                'available lots' : 'NA',
            }

            # Get the number of lots available
            if carpark.main_table.carpark_available_lot:
                parking_details['available lots'] = carpark.main_table.carpark_available_lot[0].lots_available
            
            nearby_carpark_list.append(parking_details)
    # Checking if there are nearby carparks or not
    if nearby_carpark_list:
        # Filtering the Nearby Carparks
        filtered_carpark = filter_nearby_carparks(nearby_carpark_list)
        # Getting the list for the to create inline_buttons
        inline_btn_list = create_inline_values_filter_carpark(filtered_carpark)
        return inline_btn_list, filtered_carpark
    else:
        return False, False

def create_inline_values_filter_carpark(filtered_carpark):
    inline_btn_list = []
    for carpark in filtered_carpark:
        btn_info = {
            'text' : carpark['carpark'].pp_name,
            'callback_data': carpark['carpark'].pp_code,
        }
        inline_btn_list.append(btn_info)

    return inline_btn_list

def filter_nearby_carparks(nearby_carpark_list):
    sorted_carpark = carpark_sort_by_distance(nearby_carpark_list)
    if len(sorted_carpark) > 5:
        sorted_carpark = get_nearest_five(sorted_carpark)

    return sorted_carpark

def carpark_sort_by_distance(nearby_carpark_list):
    # Sort using distance
    nearby_carpark_list.sort(key=lambda carpark_info: carpark_info.get('distance'))
    
    return nearby_carpark_list

def get_nearest_five(sorted_carpark):
    return nearby_carpark_list[:4]

def nearby_carpark_message(nearby_carpark_list):
    text = 'Nearby Carparks\n\n'
    
    for index, carpark in enumerate(nearby_carpark_list):
        text += 'Carpark: {}\n'.format(carpark['carpark'].pp_name)
        text += 'Distance: {}m\n'.format(round(float(carpark['distance'])*1000))
        text += 'Available Lots: {}\n\n'.format(carpark['available lots'])
    
    return text

def individual_carpark_info_text(pp_name,indv_carpark_obj):
    text = '{}\n\n'.format(pp_name)
    text += 'Price: {}/{}\n'.format(indv_carpark_obj['rate'], indv_carpark_obj['min'])
    text += 'Capacity: {}\n'.format(indv_carpark_obj['park_capacity'])
    text += 'System: {}\n\n'.format(indv_carpark_obj['parking_system'])
    if indv_carpark_obj:
        remark = indv_carpark_obj['remarks']
    else:
        remark = '-'
    text += 'Remarks: {}'.format(remark)

    return text

def current_parking_info(indv_carpark_obj):
    current_time = DateTimeFunc.current_time()
    current_day_of_week = DateTimeFunc.current_day_of_week()

    parking_info = None

    # If there is only 1 set of info i'll just provide that
    if len(indv_carpark_obj.carpark_info) > 1:
        for carpark_info in indv_carpark_obj.carpark_info:
            if carpark_info.end_time >= current_time and current_time >= carpark_info.start_time:
                parking_info = info_based_on_day_of_week(current_day_of_week, carpark_info)
    else:
        parking_info = info_based_on_day_of_week(current_day_of_week,indv_carpark_obj.carpark_info[0])
            
    return parking_info

def info_based_on_day_of_week(current_day_of_week, carpark_info):
    if current_day_of_week in range(5):
        parking_info = parking_info_dict(
            carpark_info.weekday_rate,
            carpark_info.weekday_min,
            carpark_info.parking_system,
            carpark_info.park_capacity,
            carpark_info.remarks,
        )
    elif current_day_of_week == 5:
        parking_info = parking_info_dict(
            carpark_info.satday_rate,
            carpark_info.satday_min,
            carpark_info.parking_system,
            carpark_info.park_capacity,
            carpark_info.remarks,
        )
    elif current_day_of_week == 6:
        parking_info = parking_info_dict(
            carpark_info.sun_ph_rate,
            carpark_info.sun_ph_min,
            carpark_info.parking_system,
            carpark_info.park_capacity,
            carpark_info.remarks,
        )

    return parking_info

def parking_info_dict(rate, time, parking_system, park_capacity, remarks=''):
    if parking_system == "C":
        parking_system = 'Coupon Parking System'
    else:
        parking_system = 'Electronic Parking System'

    current_info_dict = {
        'rate' : rate,
        'min' : time,
        'parking_system' : parking_system,
        'park_capacity' : park_capacity,
        'remarks' : remarks,
    }

    return current_info_dict
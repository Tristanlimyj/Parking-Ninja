def create_google_link(lot_object):
    carpark =  lot_object.carpark_geometry[0]
    link = 'https://www.google.com/maps/search/?api=1&query={},{}'.format(carpark.easting, carpark.northing)

    return link
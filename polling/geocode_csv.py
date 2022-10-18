'''
This is a simple utility that accepts a csv
file of address, city pairs and outputs
the values with lat, lng pairs appended
'''

import googlemaps
import csv
from secret_keys import google_api_key

glookup = googlemaps.Client(key=google_api_key)

sign_locations = []


def get_response(address):
    return glookup.geocode(address)


with open('sign_addresses.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        a = f'{row[0]}, {row[1]}, ONTARIO, CANADA'
        r = get_response(a)
        codes = r[0]['geometry']['location']
        l_l = (codes['lat'], codes['lng'])
        code_str = f'{row[0]},{row[1]},{l_l[0]},{l_l[1]}'
        print(code_str)
        sign_locations.append(code_str)


with open('coded_sign_locations.csv', mode='w') as sign_file:
    sign_writer = csv.writer(sign_file, delimiter=',')
    for location in sign_locations:
        sign_writer.writerow(location.split(','))

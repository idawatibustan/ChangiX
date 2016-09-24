import requests

# Read the api key
with open('sitakeys/airportapikey.txt') as key:
    sitakey = key.readline().strip()

url = 'https://airport.api.aero/airport'

def get_airport_details_by_code(airport_code):
    url_path = '/' + airport_code
    headers = {'Accept': 'application/json'}
    params = {'user_key': sitakey}
    r = requests.get(url + url_path, headers=headers, params=params)
    r = r.json()

    city = r['airports'][0]['city']
    code = r['airports'][0]['code']
    name = r['airports'][0]['name']
    country = r['airports'][0]['country']
    lat = r['airports'][0]['lat']
    lng = r['airports'][0]['lng']
    timezone = r['airports'][0]['timezone']
    airpot_details = {'city':city, 'code':code, 'name':name, 'country': country,
    'lat':lat, 'lng':lng, 'timezone':timezone}
    return airpot_details

import requests

# Read the api key
with open('sitakeys/flightinfoapikey.txt') as key:
    sitakey = key.readline().strip()

url_flights = 'https://flifo-qa.api.aero/flifo/v3/flights'
url_flight = 'https://flifo-qa.api.aero/flifo/v3/flight'

# Get the flight record on the current day. flight_number as in 602 of SQ602
def get_departing_info_by_flight_num(depart_airport_code, airline_code, flight_number):
    url_path = '/' + depart_airport_code + '/' + airline_code + '/' + flight_number + '/d'
    headers = {'Accept': 'application/json', 'X-apiKey': sitakey}
    r = requests.get(url_flight + url_path, headers=headers)
    r = r.json()

    airport_code = r['airportCode']
    airline = r['flightRecord'][0]['operatingCarrier']['airline']
    airline_code = r['flightRecord'][0]['operatingCarrier']['airlineCode']
    flight_number = r['flightRecord'][0]['operatingCarrier']['flightNumber']
    flight_date = r['flightDate']
    arrival_airport_code = r['flightRecord'][0]['airportCode']
    aircraft_model = r['flightRecord'][0]['aircraft']
    status_code = r['flightRecord'][0]['status']
    status = r['flightRecord'][0]['statusText']
    scheduled_time = r['flightRecord'][0]['scheduled']
    arrival_city = r['flightRecord'][0]['city']
    flight_duration_mins = r['flightRecord'][0]['duration']
    terminal = r['flightRecord'][0]['terminal']
    flight_details = {'airport_code': airport_code,
    'airline': airline, 'airline_code': airline_code,
    'flight_number': flight_number, 'flight_date': flight_date,
    'arrival_airport_code': arrival_airport_code, 'aircraft_model': aircraft_model,
    'status_code': status_code, 'status': status, 'scheduled_time': scheduled_time,
    'arrival_city': arrival_city, 'flight_duration_mins': flight_duration_mins,
    'terminal': terminal}
    return flight_details

# Get the flight records on the current day for next 4 hours
#def get_departing_infos_by_airport():

# Get the flight records on the current day for next 2 hours.
#def get_departing_infos_by_airline():

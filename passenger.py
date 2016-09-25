#!/usr/bin/env python
from datetime import datetime
from airportapihelper import *
from flightinfoapihelper import *

class Passenger:
    def __init__(self, raw_barcode_string):
        # For demo, raw_barcode_string is None
        b = barcode_decoder(raw_barcode_string)

        # Info from barcode
        self.uid = "432"
        self.firstname = b.get('firstname', "Idawati")
        self.lastname = b.get('lastname', "Bustan")
        self.origin = b.get('origin', "SIN")
        self.dest = b.get('destination', "CGK")
        self.airlines = b.get('airlines', "SQ")
        self.flightnum = b.get('flightnum', "958")
        self.date = b.get('date', '1')
        self.seat = b.get('seat', '1A')
        self.seq = b.get('seq', '23')

        self.starttime = datetime.now()

        # Populate location
        self.startloc = None
        self.currloc = None
        if raw_barcode_string is None: # Demo
            self.startloc = None # Put some demo data
            self.currloc = None # Put some demo data

        # Fetch from Airport API
        self.originname = None
        self.destname = None
        if raw_barcode_string is None: # Demo
            self.originname = 'Singapore Changi'
            self.destname = 'Jakarta-Soekarno-Hatta Int\'l'
        else:
            self.updateairportname()

        # Populate flight status
        self.boardtime = None
        self.depttime = None
        self.gate = None
        if raw_barcode_string is None: # Demo
            self.boardtime = datetime.now() # Put some demo data
            self.depttime = datetime.now() # Put some demo data
            self.gate = "34"
        else:
            self.updateflight()

    def updateflight(self):
        # Only called when data is read from real barcode
        f = get_departing_info_by_flight_num(self.origin, self.airlines, self.flightnum)
        self.boardtime = f.get('scheduled_time', 'info unavailable')
        self.depttime = f.get('scheduled_time', 'info unavailable')
        self.gate = f.get('gate', 'info unavailable')
        if self.gate is None:
            self.gate = "info unavailable"

    def time_to_board(self):
        return self.boardtime - datetime.now()

    def updateairportname(self):
        # Only called when data is read from real barcode
        self.originname = get_airport_details_by_code(self.origin).get('name', 'info unavailable')
        self.destname = get_airport_details_by_code(self.dest).get('name', 'info unavailable')

def barcode_decoder(raw_barcode_string):
    if not (raw_barcode_string is None):
        # As per IATA 2D Boarding pass format. See http://www.iata.org/whatwedo/stb/documents/bcbp_implementation_guidev4_jun2009.pdf
        passenger_name = raw_barcode_string[2:22].strip()
        origin = raw_barcode_string[30:33].strip()
        destination = raw_barcode_string[33:36].strip()
        airlines = raw_barcode_string[36:39].strip()
        flightnum = raw_barcode_string[39:44].strip()
        date = raw_barcode_string[44:47].strip()
        seat = raw_barcode_string[48:52].strip()
        seq = raw_barcode_string[52:57].strip()
        passengerstatus = raw_barcode_string[57:58].strip()
        return dict({'firstname': passenger_name[passenger_name.index('/')+1:],
                    'lastname': passenger_name[:passenger_name.index('/')],
                    'origin': origin,
                    'destination': destination,
                    'airlines': airlines,
                    'flightnum': flightnum,
                    'date': date, # 209 means 209th day of the year
                    'seat': seat,
                    'seq': seq,
                    'passengerstatus': passengerstatus})
    else:
        return {}

if __name__ == '__main__':
    p = Passenger(None)

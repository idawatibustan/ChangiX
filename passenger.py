#!/usr/bin/env python
from datetime import datetime
from airportapihelper import *
from flightinfoapihelper import *

class Passenger:
    def __init__(self, info, demo = False):
        # For demo, raw_barcode_string is None
        self.is_demo = demo
        if not self.is_demo and not (info == None):
            self.id_type = info.get('id_type')
            if self.id_type == "barcode":
                b = barcode_decoder(info.get('data'))
            elif self.id_type == "booking_ref":
                b = bookref_retriever('data')
            else:
                b = barcode_decoder(None)
        else:
            b = barcode_decoder(None)

        # Info from barcode
        self.uid = "432"
        self.firstname = b.get('firstname', "Idawati")
        self.lastname = b.get('lastname', "Bustan")
        self.origin = b.get('origin', "SIN")
        self.dest = b.get('destination', "CGK")
        self.airlines = b.get('airlines', "SQ")
        self.flightnum = b.get('flightnum', "956")
        # self.date = b.get('date', '1')
        self.seat = b.get('seat', "1A")

        self.starttime = datetime.now()
        # Populate location
        self.startgate = "B3"
        # self.currloc = None
        # if raw_barcode_string is None: # Demo
        #     self.startloc = None # Put some demo data
        #     self.currloc = None # Put some demo data

        # Fetch from Airport API
        self.originname = None
        self.destname = None
        self.updateairportname()

        # Populate flight status
        self.boardtime = None
        self.depttime = None
        self.gate = None
        self.updateflight()

    def updateflight(self):
        # Only called when data is read from real barcode
        f = get_departing_info_by_flight_num(self.origin, self.airlines, self.flightnum)
        fmt = "%Y-%m-%dT%H:%M:%S"
        self.depttime = datetime.strptime(f.get('scheduled_time', 'info unavailable')[:18], fmt)
        self.boardtime = self.depttime
        self.gate = f.get('gate', 'info unavailable')
        if self.gate is None:
            self.gate = "info unavailable"

    def time_to_board(self):
        self.updateflight()
        return (self.boardtime - datetime.now()).seconds/60

    def time_to_depart(self):
        self.updateflight()
        return (self.depttime - datetime.now()).seconds/60

    def updateairportname(self):
        # Only called when data is read from real barcode
        self.originname = get_airport_details_by_code(self.origin).get('name', 'info unavailable')
        self.destname = get_airport_details_by_code(self.dest).get('name', 'info unavailable')

    def get_arrival_gate(self):
        return {
            'gate': "B3",
            'time': datetime.now(),
            'flight': "SQ860",
            'from': "Seoul"
        }

    def get_dest_gate(self):
        self.updateflight()
        if(self.gate == None):
            self.gate = "A8"
        return {
            'gate': self.gate,
            'time': datetime.now(),
            'flight': (self.airlines+self.flightnum),
            'to': "Jakarta"
        }

def barcode_decoder(raw_barcode_string):
    if raw_barcode_string:
        # As per IATA 2D Boarding pass format. See http://www.iata.org/whatwedo/stb/documents/bcbp_implementation_guidev4_jun2009.pdf
        # passenger_name = raw_barcode_string[2:22].strip()
        # origin = raw_barcode_string[30:33].strip()
        # destination = raw_barcode_string[33:36].strip()
        # airlines = raw_barcode_string[36:39].strip()
        # flightnum = raw_barcode_string[39:44].strip()
        # date = raw_barcode_string[44:47].strip()
        # seat = raw_barcode_string[48:52].strip()
        # seq = raw_barcode_string[52:57].strip()
        # passengerstatus = raw_barcode_string[57:58].strip()
        # return dict({'firstname': passenger_name[passenger_name.index('/')+1:],
        #             'lastname': passenger_name[:passenger_name.index('/')],
        #             'origin': origin,
        #             'destination': destination,
        #             'airlines': airlines,
        #             'flightnum': flightnum,
        #             'date': date, # 209 means 209th day of the year
        #             'seat': seat,
        #             'seq': seq,
        #             'passengerstatus': passengerstatus})
        return dict({'firstname': "Juho",
                    'lastname': "Lee",
                    'origin': "HKG",
                    'destination': "SFO",
                    'airlines': "CX",
                    'flightnum': "870",
                    'seat': "49E" })
    else:
        return dict()

def bookref_retriever(data):
    return barcode_decoder(None)

if __name__ == '__main__':
    p = Passenger(None, True)

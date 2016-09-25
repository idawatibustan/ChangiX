#!/usr/bin/env python
from datetime import datetime
# import barcode_reader
# import flight_reader

class Passenger:
    def __init__(self, id):
        b = barcode_decoder("M1LEE/JUHO            E8EKVV7 SINHKGCX 0710 209Y056K0224 34A&gt;1180      B                29                                         8")

        self.uid = "432"
        self.firstname = b.get('firstname', "Jane")
        self.lastname = b.get('lastname', "Doe")
        self.origin = b.get('origin', "AAA")
        self.dest = b.get('destination', "ZZZ")
        self.airlines = b.get('airlines', "XX")
        self.flightnum = b.get('flightnum', "123")
        self.date = b.get('date')
        self.seat = b.get('seat')
        self.seq = b.get('seq')

        self.starttime = datetime.now()
        self.startloc = None
        self.currloc = None
        self.boardtime = None
        self.depttime = None
        self.gate = None

        self.updateflight()

    def updateflight(self):
        f = self.flight_reader(self.flightnum)
        self.boardtime = f.get('boardingtime')
        self.depttime = f.get('departtime')
        self.gate = f.get('gate')

    def time_to_board(self):
        return self.boardtime - datetime.now()

    def flight_reader(self, num):
        return dict({'boardingtime': datetime.now(),
                    'departtime': datetime.now(),
                    'gate': "5D" })

def barcode_decoder(raw_barcode_string):
    # As per IATA 2D Boarding pass format. See http://www.iata.org/whatwedo/stb/documents/bcbp_implementation_guidev4_jun2009.pdf
    passenger_name = raw_barcode_string[2:22].strip()
    origin = raw_barcode_string[30:33].strip()
    destination = raw_barcode_string[33:36].strip()
    airline = raw_barcode_string[36:39].strip()
    flightnum = raw_barcode_string[39:44].strip()
    date = raw_barcode_string[44:47].strip()
    seat = raw_barcode_string[48:52].strip()
    seq = raw_barcode_string[52:57].strip()
    passengerstatus = raw_barcode_string[57:58].strip()
    return dict({'firstname': passenger_name[passenger_name.index('/')+1:],
                'lastname': passenger_name[:passenger_name.index('/')],
                'origin': origin,
                'destination': destination,
                'airline': airline,
                'flightnum': flightnum,
                'date': date, # 209 means 209th day of the year
                'seat': seat,
                'seq': seq,
                'passengerstatus': passengerstatus})

if __name__ == '__main__':
    p = Passenger(None)

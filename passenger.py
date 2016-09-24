#!/usr/bin/env python
from datetime import datetime
# import barcode_reader
# import flight_reader

class Passenger:
    def __init__(self, id):
        b = barcode_reader(id)

        self.name = b.get('firstname', "Jane") + " " + b.get('lastname', "Doe")
        self.origin = b.get('origin', "AAA")
        self.dest = b.get('destination', "ZZZ")
        self.flightnum = b.get('airlines', "XX")
        self.date = b.get('date')
        self.seat = b.get('seat')
        self.seq = b.get('seq')

        self.starttime = datetime.now()
        self.startloc = None
        self.currloc = None
        self.boardtime = None
        self.depttime = None
        self.boardgate = None

        self.updateflight()

    def updateflight(self):
        f = flight_reader(self.flightnum)
        self.boardtime = f.boardingtime
        self.depttime = f.departtime
        self.boardgate = flight.gate
#!/usr/bin/env python
from datetime import datetime
# import barcode_reader
# import flight_reader

class Passenger:
    def __init__(self, id):
        b = self.barcode_reader(id)

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
        f = self.flight_reader(self.flightnum)
        self.boardtime = f.get('boardingtime')
        self.depttime = f.get('departtime')
        self.boardgate = flight.gate

    def barcode_reader(id):
        return dict({'firstname': "Juho",
                    'lastname': "Lee",
                    'origin': "DUB",
                    'destination': "SIN",
                    'airlines': "SQ",
                    'date': "25Sept",
                    'seat': "1A",
                    'seq': 23 })

    def flight_reader(num):
        return dict({'boardingtime': datetime.now(),
                    'departtime': datetime.now() })
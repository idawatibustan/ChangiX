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

def barcode_decoder(id):
    id = id.split()
    print id
    for i in id:
        #parse i here = just harcode the format

    return dict({'firstname': "Janet",
                'lastname': "Lee",
                'origin': "KOR",
                'destination': "SIN",
                'airlines': "SQ",
                'flightnum': "316",
                'date': "25Sept",
                'seat': "1A",
                'seq': 23 })

if __name__ == '__main__':
    p = Passenger(None)

#M1LEE/JUHO            E8EKVV7 SINHKGCX 0710 209Y056K0224 34A&gt;1180      B                29                                         8
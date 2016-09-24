#!/usr/bin/env python

class Shopping:
    def __init__(self, cps):
        self.shoppes = []
        self.items = []
        self.checkretail(cps)
        self.status = None

    def hasretail(self):
        if len(shoppes) == 0:
            return False
        return True

    def checkretail(self, cps):
        for cp in cps:
            if cp.category == 'Retail':
                self.shoppes.append(cp.name)

    def loaditems(self):
        for shop in self.shoppes:
            items = shop.top_five()

class Purchases:
    def __init__(self):
        self.status = None
        # processed, dispatched, delivered
        self.items = []
        self.totalprice = 0.00

    def additem(self, item):
        self.items.append(item)
        self.totalprice += item.price

    def checkout(self):
        self.status = 'processed'
        return self.totalprice

    def isprocessed():
        return self.status == 'processed'

    def isdispatched():
        return self.status == 'dispatched'

    def isdelivered():
        return self.status == 'delivered'

class Shop:
    def __init__(self):
        self.name = None
        self.items = []
    
    def populate_items(self):
        self.items = [{
            Item('Chanel', 'Coco Au De Perfume', 72.00, 'img\\1.jpg'),
            Item('DKNY', 'Fresh Blossom 100ml', 69.00, ''),
            Item('Lancome' 'Miracle', 99.00, ''),
            Item('Yves Saint Laurent','Black Opium EDP', 105.00, ''),
            Item('Marc Jacobs', 'Daisy EDT', 93.00, ''),
        }]

    def top_five(self):
        return self.items[0:4]

class Item:
    def __init__(self, brand, name, price, image):
        self.brand = None
        self.name = None
        self.price = None
        self.image = None
        self.status = 'standard'
        #promo, exclusive, standard
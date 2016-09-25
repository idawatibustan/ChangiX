#!/usr/bin/env python
import json

class Shopping:
    def __init__(self, checkpoints_liked):
        retail_checkpoints = filter(lambda cp: cp['category']=='Retail', checkpoints_liked)
        self.shop_items = self._process(retail_checkpoints)
        self.bought = []

    def _process(self, retail_checkpoints):
        if retail_checkpoints:
            catalog = json.loads(open("json/catalog.json").read())
            shop_names = [chp['name'] for chp in retail_checkpoints]
            items = []
            for shop_name in shop_names:
                items.extend(catalog[shop_name])
            items = sorted(items, key=lambda x: x['price'], reverse=True)
            return items
        return None

    def buy(self, item):
        self.bought.append(item)

    def get_list(self, top=5):
        lst = []
        curr_count = 0
        if self.shop_items:
            for item in self.shop_items:
                curr_count += 1
                status = 'bought' if item in self.bought else 'not_bought'
                item['status'] = status
                lst.append(item)
                if curr_count == top:
                    return lst
                elif curr_count > top:
                    raise Exception("How in the world did this happen")
        return None

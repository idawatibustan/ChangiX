from Queue import Queue
from itertools import cycle
from random import shuffle
import json

class Recommender:
    def __init__(self, passenger=None, demo=False):
        '''
        For demo purposes, initalize the class with the demo parameter:
        r = Recommender(passenger, demo=True)
        '''
        self.passenger = passenger
        self.is_demo = demo
        self.checkpoints_liked = []
        self.categories_disliked = []
        checkpoints = generate_checkpoints(demo)
        self.q = self._sort(checkpoints)

    def checkpoint_info(self):
        return None if self.q.empty() else self.q.get()

    def like_checkpoint(self, checkpoint):
        self.checkpoints_liked.append(checkpoint)

    def dislike_checkpoint(self, checkpoint):
        category = checkpoint['category']
        self.categories_disliked.append(category)

        # create new queue without the disliked category
        new_q = Queue()
        while not self.q.empty():
            curr_checkpoint = self.q.get()
            if curr_checkpoint['category'] not in self.categories_disliked:
                new_q.put(curr_checkpoint)
        self.q = new_q

    def recommendations(self):
        return self.checkpoints_liked

    def _sort(self, checkpoints):
        q = Queue()
        if self.is_demo:
            [q.put(c) for c in checkpoints]
        else:
            # creates circular list of the unique categories
            categories = cycle(set(c['category'] for c in checkpoints))

            # format checkpoints into a dictionary where keys are the categories, and values are the checkpoints belonging to that category
            chk_by_cat = {}
            for checkpoint in checkpoints:
                cat = checkpoint['category']
                if cat in chk_by_cat:
                    chk_by_cat[cat].append(checkpoint)
                else:
                    chk_by_cat[cat] = [checkpoint]

            # create new queue where the order of elements cycle equally across the categories
            while self._not_empty(chk_by_cat):
                curr_cat = categories.next()
                checkpoints_from_cat = chk_by_cat[curr_cat]
                if checkpoints_from_cat:
                    shuffle(checkpoints_from_cat)
                    checkpoint = checkpoints_from_cat.pop()
                else:
                    checkpoint = None
                chk_by_cat[curr_cat] = checkpoints_from_cat
                if checkpoint:
                    q.put(checkpoint)
        return q

    def _not_empty(self, d):
        return len([item for sublist in d.values() for item in sublist]) != 0

def generate_checkpoints(is_demo):
    if is_demo:
        checkpoints = json.loads(open("json/demo_checkpoints.json").read())
    else:
        checkpoints = json.loads(open("json/production_checkpoints.json").read())
    return checkpoints

if __name__=="__main__":
    r = Recommender(None, demo=False)
    r.dislike_checkpoint({'category':'Retail'})
    boo = True
    while boo:
        cc = r.checkpoint_info()
        if not cc:
            boo = False
        else:
            print cc['name']

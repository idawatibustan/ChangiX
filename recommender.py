from Queue import Queue

class Recommender:
    def __init__(self, passenger):
        self.passenger = passenger
        checkpoints = generate_checkpoints()
        checkpoints = [Checkpoint(c['name'], c['category'], c['subcategory']) for c in checkpoints]
        self.q = self._sort(checkpoints)
        self.checkpoints_liked = []
        self.categories_disliked = []

    def checkpoint_info(self):
        return None if self.q.empty() else self.q.get().as_dict()

    def like_checkpoint(self, checkpoint):
        self.checkpoints_liked.append(checkpoint)

    def dislike_checkpoint(self, checkpoint):
        category = checkpoint['category']
        self.categories_disliked.append(category)

    def recommendations(self):
        return self.checkpoints_liked

    def _sort(self, checkpoints):
        q = Queue()
        [q.put(c) for c in checkpoints]
        return q


class Checkpoint:
    def __init__(self, name, category, subcategory):
        self.name = name
        self.category = category
        self.subcategory = subcategory

    def __str__(self):
        return "%s (%s: %s)" % (self.name, self.category, self.subcategory)
    def __unicode__(self):
        return "%s (%s: %s)" % (self.name, self.category, self.subcategory)
    def __repr__(self):
        return "%s (%s: %s)" % (self.name, self.category, self.subcategory)

    def as_dict(self):
        return {
            'name': self.name,
            'category': self.category,
            'subcategory': self.subcategory
        }

def generate_checkpoints():
    return [
        {
            'name': 'Ajisen Ramen',
            'category': 'Food',
            'subcategory': 'Japanese',
        }, {
            'name': 'Indonesian Barbequeue',
            'category': 'Food',
            'subcategory': 'Indonesian'
        }, {
            'name': 'Giant Slide',
            'category': 'Leisure',
            'subcategory': 'Entertainment'
        }, {
            'name': 'Coco Chanel',
            'category': 'Retail',
            'subcategory': 'Cosmetics'
        }, {
            'name': 'Airport Wellness Oasis',
            'category': 'Leisure',
            'subcategory': 'Relaxation'
        }
    ]

if __name__=="__main__":
    r = Recommender(None)
    print r.checkpoint_info()

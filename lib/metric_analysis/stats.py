
class Stats(object):
    def __init__(self):
        self.true_positive = 0
        self.true_negative = 0
        self.false_positive = 0
        self.false_negative = 0

    def __repr__(self):
        return "Stats[ true_positive = {}, true_negative = {}, false_positive = {}, false_negative = {}]".format(
            self.true_positive, self.true_negative, self.false_positive, self.false_negative)

    def __str__(self):
        return "Stats[ true_positive = {}, true_negative = {}, false_positive = {}, false_negative = {}]".format(
            self.true_positive, self.true_negative, self.false_positive, self.false_negative)

from collections.abc import Iterable

from entity.Foreldri import Foreldri


# foreldrar sem fá auka þrif
class PriorityListIterator(Iterable):

    def __init__(self, foreldralisti: [Foreldri]):
        self.i = 0
        self.foreldralisti = foreldralisti

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i >= len(self.foreldralisti):
            return None
        f = self.foreldralisti[self.i]
        self.i += 1
        return f

    def reset(self):
        self.i = 0


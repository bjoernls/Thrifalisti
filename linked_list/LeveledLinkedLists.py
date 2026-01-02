from entity.Foreldri import Foreldri
from entity.PriorityList import PriorityListIterator
from entity.Strategy import RandomStrategy
from linked_list.LinkedList import LinkedList


class LeveledLinkedLists:

    def __init__(self, foreldralisti: [Foreldri]):
        self.__init_linked_lists(foreldralisti)
        self.level = 0
        self.curr_lllist: LinkedList = self.all_llls[self.level]
        self.tmp_foreldri = None
        self.__retry_pile = []
        self.__deadlock = False

    def __init_linked_lists(self, foreldralisti: [Foreldri]):
        self.all_llls = [LinkedList([], RandomStrategy())]
        self.all_llls += [LinkedList([], RandomStrategy())]

        priority_list = []
        for f in foreldralisti:
            if f.has_auka_thrif():
                priority_list += [f]
            else:
                while len(self.all_llls) < f.get_count() + 1:
                    self.all_llls += [LinkedList([], RandomStrategy())]
                self.all_llls[f.get_count()].push(f)

        self.priority_list_iterator = PriorityListIterator(priority_list)

    def pop(self):
        self.tmp_foreldri = next(self.priority_list_iterator)

        if not self.tmp_foreldri:
            self.tmp_foreldri = self.curr_lllist.pop_strategy()

        if self.curr_lllist.is_empty():
            if self.__retry_pile:
                self.__deadlock = True
            self.__increase_level()

        return self.tmp_foreldri

    def __increase_level(self):
        self.level += 1
        self.curr_lllist = self.all_llls[self.level]
        self.priority_list_iterator.reset()
        self.all_llls += [LinkedList([], RandomStrategy())]

    def discard(self):
        self.tmp_foreldri = None

    def commit(self):
        self.all_llls[self.level + 1].push(self.tmp_foreldri)
        self.tmp_foreldri = None

    # þegar það er ekki nógu langt bil á milli þrifa
    def retry(self):
        self.__retry_pile += [self.tmp_foreldri]
        self.tmp_foreldri = None

    def is_deadlock(self):
        return self.__deadlock

    def reset_deadlock(self):
        self.__deadlock = False
        for f in self.__retry_pile:
            self.curr_lllist.push(f)

    def get_retry_pile(self):
        return self.__retry_pile

from math import ceil, floor

from control.AlgorithmException import MaximumAllocationsExceededException, MinVikubilNotMetException
from control.Thrifalisti import Thrifalisti
from entity.Foreldri import Foreldri
from linked_list.LeveledLinkedLists import LeveledLinkedLists
from control.AlgorithmException import MaximumAllocationsExceededException, MinVikubilNotMetException


def get_min_vikubil(vika, vikur):
    return min([abs(v - vika.get_vika_nr()) for v in vikur])


class ThrifalistiAlgo:

    def __init__(self, foreldralisti: [Foreldri], config):
        self.__leveled_linked_lists = LeveledLinkedLists(foreldralisti)
        self.min_vikubil = config.getint('MinVikubil')
        self.maximum_allocations = config.getint('MaximumAllocations')

    def __calc_max_level(self, foreldralisti, huslisti, viku_fjoldi):
        return ceil(float(len(huslisti) * viku_fjoldi) / len(foreldralisti)) + 1

    def compute(self, thrifalisti: Thrifalisti):
        while not thrifalisti.is_full():
            if self.__is_deadlock():
                self.__resolve_deadlock(thrifalisti)
            foreldri = self.__leveled_linked_lists.pop()

            alloc_found = self.__find_alloc(foreldri, thrifalisti)

            if not alloc_found:
                self.__leveled_linked_lists.retry()
                continue
            elif foreldri.is_done():
                self.__leveled_linked_lists.discard()
            else:
                self.__leveled_linked_lists.commit()
        return True

    def __find_alloc(self, foreldri, thrifalisti):
        for vikuthrifalisti in self.__get_vikur_ekki_of_nalaegt(thrifalisti, foreldri):
            if self.__try_set_foreldri(foreldri, vikuthrifalisti):
                return True
        return False

    def __get_vikur_ekki_of_nalaegt(self, thrifalisti, foreldri):
        min_distance = self.__calc_min_vikubil(thrifalisti)
        return list(filter(lambda vika: not self.is_of_nalaegt(foreldri.get_vikur(), vika, min_distance),
                           list(filter(lambda v: not v.is_fri(), thrifalisti.get_vikuthrifalistar()))))

    def is_of_nalaegt(self, foreldri_vikur, vikuthrifalisti, min_vikubil):
        if len(foreldri_vikur) == 0:
            return False
        return any([abs(v - vikuthrifalisti.get_vika_nr()) < min_vikubil for v in foreldri_vikur])

    def __is_deadlock(self):
        return self.__leveled_linked_lists.is_deadlock()

    def __resolve_deadlock(self, thrifalisti):
        retry_pile = list(self.__get_retry_pile().copy())

        avail_vikur = list(filter(lambda v: not v.is_full(), thrifalisti.get_vikuthrifalistar()))

        for vikuthrifalisti in avail_vikur:
            foreldri = self.__set_foreldri_with_max_vikubil(retry_pile, vikuthrifalisti)
            if not foreldri:
                continue
            retry_pile.remove(foreldri)
            if len(retry_pile) == 0:
                break

        self.__leveled_linked_lists.reset_deadlock()

    def __get_retry_pile(self):
        return self.__leveled_linked_lists.get_retry_pile()


    def __set_foreldri_with_max_vikubil(self, retry_pile, vikuthrifalisti):
        retry_pile.sort(key=lambda foreldri: get_min_vikubil(vikuthrifalisti, foreldri.get_vikur()), reverse=True)
        for f in retry_pile:
            if self.__try_set_foreldri(f, vikuthrifalisti):
                return f
        return None

    def __try_set_foreldri(self, foreldri, vikuthrifalisti):
        if vikuthrifalisti.try_set_foreldri(foreldri):
            if foreldri.get_count() > self.maximum_allocations:
                raise MaximumAllocationsExceededException
            vikubil = foreldri.get_vikubil()
            if 0 < vikubil < self.min_vikubil:
                raise MinVikubilNotMetException
            return foreldri

    def __calc_min_vikubil(self, thrifalisti):
        viku_fjoldi = len(list(filter(lambda v: not v.is_fri(), thrifalisti.get_vikuthrifalistar())))
        return floor(viku_fjoldi / 2)

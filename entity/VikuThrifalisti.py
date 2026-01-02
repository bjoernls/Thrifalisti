from random import shuffle

from entity.Allocation import Allocation
from entity.Vika import Vika


class VikuThrifalisti:
    def __init__(self, vika_nr, vika_texti, thrifalisti_fyrir_viku, non_exclusive_husalisti):
        self.__thrifalisti_fyrir_viku = thrifalisti_fyrir_viku
        self.__vika = Vika(vika_nr, vika_texti)
        self.__non_exclusive_husalisti = non_exclusive_husalisti

    def __sub__(self, other):
        return self.__vika.get_nr() - other.get_vika_nr()

    def is_fri(self):
        return self.__vika.is_fri()

    def get_vika_nr(self):
        return self.__vika.get_nr()

    def get_foreldri_i_husi(self, hus):
        return self.__thrifalisti_fyrir_viku[hus]

    def set_foreldri_i_husi(self, hus, foreldri):
        foreldri.add_allocation(Allocation(self.__vika, hus))
        self.__thrifalisti_fyrir_viku[hus] = foreldri

    def try_set_foreldri(self, foreldri):
        husalisti = foreldri.get_husalisti()
        shuffle(husalisti)
        for hus in husalisti:
            if not self.__thrifalisti_fyrir_viku[hus]:
                self.set_foreldri_i_husi(hus, foreldri)
                return True
        return False

        return None

    def is_full(self):
        return self.is_fri() or all([f for f in self.__thrifalisti_fyrir_viku.values()])

    def skip_hus(self, hus):
        self.__thrifalisti_fyrir_viku[hus] = "skip"

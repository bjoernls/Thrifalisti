from entity.Foreldri import Foreldri
from entity.Hus import Hus
from entity.Vika import Vika
from entity.VikuThrifalisti import VikuThrifalisti
from excel.dto.ForeldriDto import ForeldriDto
from excel.dto.ThrifalistiDto import ThrifalistiDto
from excel.dto.YfirlitDto import YfirlitDto


class Mapper:

    def map_to_entity(self, dto):
        raise NotImplementedError

    def map_to_dto(self, entity):
        raise NotImplementedError

    def reset(self):
        pass


class HusMapper(Mapper):
    def map_to_entity(self, hus_dto):
        return Hus(hus_dto.get_nafn(), exklusift=hus_dto.is_exclusive())


class YfirlitMapper(Mapper):

    def map_to_dto(self, foreldri):
        return YfirlitDto(foreldri.get_nafn(), foreldri.get_count(), foreldri.get_allocations())


class ForeldriMapper(Mapper):

    def __init__(self, husalisti):
        self.husalisti = husalisti

    @staticmethod
    def __map_hus(hus_nafn, husalisti):
        return next((h for h in husalisti if h.get_nafn() == hus_nafn))

    def map_to_dto(self, entity):
        pass

    def map_to_entity(self, foreldri_dto: ForeldriDto) -> Foreldri:
        husalisti_mapped = list(map(lambda h: self.__map_hus(h, self.husalisti), foreldri_dto.get_husalisti()))
        if len(husalisti_mapped) == 0:
            husalisti_mapped = list(filter(lambda h: not h.is_exclusift(), self.husalisti))
        return Foreldri(foreldri_dto.get_nafn(), husalisti_mapped, foreldri_dto.get_thrifastada(), foreldri_dto.has_less_thrif(),
                        foreldri_dto.has_auka_thrif())


class ThrifalistiMapper(Mapper):

    def __init__(self, husalisti, foreldralisti, columns, col_to_hus_map):
        self.vika_nr = 0
        self.__husalisti = husalisti
        self.__foreldralisti = foreldralisti
        self.__columns = columns
        self.col_to_hus_map = col_to_hus_map

    def map_to_dto(self, thrifalisti_fyrir_viku):
        dto = ThrifalistiDto()
        cols = self.__columns
        for hus in self.__husalisti:
            col = next(filter(lambda c: hus.get_nafn() == self.col_to_hus_map[c.get_pos()], cols))
            foreldri_i_husi = thrifalisti_fyrir_viku.get_foreldri_i_husi(hus)
            if foreldri_i_husi and foreldri_i_husi != "skip":
                col.setter(dto, hus.get_nafn(), foreldri_i_husi.get_nafn())
            else:
                col.setter(dto, hus.get_nafn(), None)
        return dto

    def map_to_entity(self, dto):
        vikuthrifalisti = VikuThrifalisti(self.vika_nr, dto.get_vika_texti(),
                                          self.__create_new_vikuthrifalisti(), self.__get_all_non_exclusive_hus())
        self.__map_foreldri_i_thrifalisti(dto, vikuthrifalisti)
        self.vika_nr += 1
        return vikuthrifalisti

    def __map_foreldri_i_thrifalisti(self, dto, vika):
        for h in self.__husalisti:
            nafn_i_toflu = dto.get_thrif(h.get_nafn())
            if nafn_i_toflu is not None and nafn_i_toflu != "x":
                vika.set_foreldri_i_husi(h, next((f for f in self.__foreldralisti if f.get_nafn() == nafn_i_toflu)))
            if nafn_i_toflu == "x":
                vika.skip_hus(h)


    def __get_all_non_exclusive_hus(self):
        return list(filter(lambda h: not h.is_exclusift(), self.__husalisti))

    def __create_new_vikuthrifalisti(self):
        return {key: None for key in self.__husalisti}

    def reset(self):
        self.vika_nr = 0

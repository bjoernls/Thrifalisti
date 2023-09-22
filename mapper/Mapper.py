from entity.Foreldri import Foreldri
from entity.Hus import Hus
from entity.VikuThrifalisti import VikuThrifalisti
from excel.dto.Column import Column
from excel.dto.ForeldriDto import ForeldriDto
from excel.dto.ThrifalistiDto import ThrifalistiDto, ThrifalistiColumn


class Mapper:

    def map_to_entity(self, dto):
        raise NotImplementedError

    def map_to_dto(self, entity, col_map=None):
        raise NotImplementedError

    def get_columns(self):
        raise NotImplementedError

    def reset(self):
        pass


class HusMapper(Mapper):

    def __init__(self):
        self.__columns = [Column("A", lambda args: args[0].set_nafn(args[1]), lambda args: args[0].get_nafn())]
        self.__columns += [
            Column("B", lambda args: args[0].set_exclusive(args[1]), lambda args: args[0].is_exclusive())]

    def get_columns(self):
        return self.__columns

    def map_to_dto(self, entity, col_map=None):
        pass

    def map_to_entity(self, hus_dto):
        return Hus(hus_dto.get_nafn(), exklusift=hus_dto.is_exclusive())


class ForeldriMapper(Mapper):

    def get_columns(self):
        return self.columns

    def map_to_dto(self, entity, col_map=None):
        pass

    def __init__(self, husalisti):
        self.husalisti = husalisti
        self.columns = [Column("B", lambda args: args[0].set_nafn(args[1]), lambda args: args[0].get_nafn())]
        self.columns += [
            Column("C", lambda args: args[0].set_thrifastada(args[1]), lambda args: args[0].get_thrifastada())]
        self.columns += [Column("D", lambda args: args[0].add_hus(args[1]), lambda args: args[0].get_husalisti())]
        self.columns += [Column("E", lambda args: args[0].add_hus(args[1]), lambda args: args[0].get_husalisti())]
        self.columns += [Column("F", lambda args: args[0].add_hus(args[1]), lambda args: args[0].get_husalisti())]

    def __map_hus(self, hus_nafn, husalisti):
        for h in husalisti:
            if h.get_nafn() == hus_nafn:
                return h
        raise ValueError

    def map_to_entity(self, foreldri_dto: ForeldriDto) -> Foreldri:
        husalisti_mapped = list(map(lambda h: self.__map_hus(h, self.husalisti), foreldri_dto.get_husalisti()))
        if len(husalisti_mapped) == 0:
            husalisti_mapped = list(filter(lambda h: not h.is_exclusift(), self.husalisti))
        return Foreldri(foreldri_dto.get_nafn(), husalisti_mapped, foreldri_dto.has_less_thrif(),
                        foreldri_dto.has_auka_thrif())


class ThrifalistiMapper(Mapper):
    __FRI = ["Haustfrí", "Jólafrí"]

    def __init__(self, husalisti):
        self.vika_nr = 0
        self.__husalisti = husalisti

        self.columns = [
            ThrifalistiColumn("A", lambda args: args[0].set_vika_texti(args[1]), lambda dto: dto.get_vika_texti())]

        for s in range(ord("B"), ord("G") + 1):
            col_stafur = chr(s)
            self.columns += [ThrifalistiColumn(col_stafur, lambda args: args[0].add_to_thrifalisti(args[1], args[2]),
                                               lambda args: args[0].get_thrif(args[1]), is_thrif=True)]

    def get_columns(self):
        return self.columns

    def map_to_dto(self, thrifalisti_fyrir_viku, col_to_hus_map=None):
        dto = ThrifalistiDto()
        cols = self.get_columns()
        for hus in self.__husalisti:
            col = next(filter(lambda c: hus.get_nafn() == col_to_hus_map[c.get_pos()], cols))
            foreldri_i_husi = thrifalisti_fyrir_viku.get_foreldri_i_husi(hus)
            if foreldri_i_husi:
                col.setter(dto, hus.get_nafn(), foreldri_i_husi.get_nafn())
            else:
                col.setter(dto, hus.get_nafn(), None)
        return dto

    def map_to_entity(self, dto):
        vika_texti = dto.get_vika_texti()
        vika = VikuThrifalisti(self.vika_nr, vika_texti,
                               self.__is_fri(vika_texti), self.__create_new_vikuthrifalisti(),
                               self.__get_all_non_exclusive_hus())
        self.vika_nr += 1
        return vika

    def __get_all_non_exclusive_hus(self):
        return list(filter(lambda h: not h.is_exclusift(), self.__husalisti))

    def __is_fri(self, texti):
        return any(fri in texti for fri in self.__FRI)

    def __create_new_vikuthrifalisti(self):
        return {key: None for key in self.__husalisti}

    def reset(self):
        self.vika_nr = 0

from excel.Column import Column
from excel.SheetReader import SheetReader, ThrifalistiSheetReader, get_sheet_value
from excel.SheetWriter import ThrifalistiSheetWriter, YfirlitSheetWriter
from excel.dto.ForeldriDto import ForeldriDto
from excel.dto.HusDto import HusDto
from excel.dto.ThrifalistiDto import ThrifalistiDto, ThrifalistiColumn
from excel.dto.YfirlitDto import YfirlitDto
from excel.sheet_infos.ForeldriSheetInfo import ForeldriSheetInfo
from excel.sheet_infos.HusSheetInfo import HusSheetInfo
from excel.sheet_infos.ThrifalistiSheetInfo import ThrifalistiSheetInfo
from excel.sheet_infos.YfirlitSheetInfo import YfirlitSheetInfo
from mapper.Mapper import HusMapper, ForeldriMapper, ThrifalistiMapper, YfirlitMapper


class SheetHandler:

    def __init__(self, wb):
        self.__wb = wb
        self.__mapper = None
        self.__reader = None
        self.__writer = None
        self.__info = None
        self.__sheet = None

    def read(self):
        self._get_mapper().reset()
        return [self._get_mapper().map_to_entity(dto) for dto in self._get_reader().read()]

    def write(self, entities):
        return self._get_writer().write(entities)

    def _get_sheet(self):
        if not self.__sheet:
            self.__sheet = self.__wb[self._get_info().get_sheet_name()]
        return self.__sheet

    def _get_columns(self):
        raise NotImplementedError

    def _get_reader(self):
        if not self.__reader:
            self.__reader = self._init_reader()
        return self.__reader

    def _get_dto_factory(self):
        raise NotImplementedError

    def _get_writer(self):
        if not self.__writer:
            self.__writer = self._init_writer()
        return self.__writer

    def _get_mapper(self):
        if not self.__mapper:
            self.__mapper = self._init_mapper()
        return self.__mapper

    def _get_info(self):
        if not self.__info:
            self.__info = self._init_info()
        return self.__info

    def _init_writer(self):
        raise NotImplementedError

    def _init_reader(self):
        return SheetReader(self._get_sheet(), self._get_info(), self._get_columns(), self._get_dto_factory())

    def _init_info(self):
        raise NotImplementedError

    def _init_mapper(self):
        raise NotImplementedError


class HusSheetHandler(SheetHandler):

    def __init__(self, wb):
        super().__init__(wb)

    def _get_columns(self):
        columns = [Column("A", lambda args: args[0].set_nafn(args[1]), lambda args: args[0].get_nafn())]
        columns += \
            [Column("B", lambda args: args[0].set_exclusive(args[1]), lambda args: args[0].is_exclusive())]
        return columns

    def _get_dto_factory(self):
        return lambda: HusDto()

    def _init_mapper(self):
        return HusMapper()

    def _init_info(self):
        return HusSheetInfo()


columns = [
    ThrifalistiColumn("A", None, lambda args: args[0].get_nafn()),
    ThrifalistiColumn("B", None, lambda args: args[0].get_count()),

    ThrifalistiColumn("C", None, lambda args: args[0].get_alloc_hus(0)),
    ThrifalistiColumn("D", None, lambda args: args[0].get_alloc_vika(0)),

    ThrifalistiColumn("E", None, lambda args: args[0].get_alloc_hus(1)),
    ThrifalistiColumn("F", None, lambda args: args[0].get_alloc_vika(1)),

    ThrifalistiColumn("G", None, lambda args: args[0].get_alloc_hus(2)),
    ThrifalistiColumn("H", None, lambda args: args[0].get_alloc_vika(2))
]


class YfirlitSheetHandler(SheetHandler):
    def _get_columns(self):

        return columns

    def _init_writer(self):
        return YfirlitSheetWriter(self._get_sheet(), self._get_mapper(),
                                  self._get_info(), self._get_columns())

    def _init_info(self):
        return YfirlitSheetInfo()

    def _init_mapper(self):
        return YfirlitMapper()


class ForeldriSheetHandler(SheetHandler):

    def __init__(self, wb, husalisti):
        super().__init__(wb)
        self.husalisti = husalisti

    def _get_columns(self):
        columns = [Column("B", lambda args: args[0].set_nafn(args[1]), lambda args: args[0].get_nafn())]
        columns += \
            [Column("C", lambda args: args[0].set_thrifastada(args[1]), lambda args: args[0].get_thrifastada())]
        columns += [Column("D", lambda args: args[0].add_hus(args[1]), lambda args: args[0].get_husalisti())]
        columns += [Column("E", lambda args: args[0].add_hus(args[1]), lambda args: args[0].get_husalisti())]
        columns += [Column("F", lambda args: args[0].add_hus(args[1]), lambda args: args[0].get_husalisti())]
        return columns

    def _get_dto_factory(self):
        return lambda: ForeldriDto()

    def _init_mapper(self):
        return ForeldriMapper(self.husalisti)

    def _init_info(self):
        return ForeldriSheetInfo()


class ThrifalistiSheetHandler(SheetHandler):
    def __init__(self, wb, husalisti, foreldralisti):
        super().__init__(wb)
        self.foreldralisti = foreldralisti
        self.husalisti = husalisti
        self.__col_to_hus_map = {}

    def _get_dto_factory(self):
        return lambda: ThrifalistiDto()

    def _init_mapper(self):
        return ThrifalistiMapper(self.husalisti, self.foreldralisti, self._get_columns(), self.__get_col_to_hus_map())

    def _init_info(self):
        return ThrifalistiSheetInfo()

    def _init_reader(self):
        return ThrifalistiSheetReader(self._get_sheet(), self._get_info(),
                                      self._get_columns(), self._get_dto_factory(), self.__get_col_to_hus_map())

    def _init_writer(self):
        return ThrifalistiSheetWriter(self._get_sheet(), self._get_mapper(), self._get_info(), self._get_columns(),
                                      self.__get_col_to_hus_map())

    def _get_columns(self):
        columns = [
            ThrifalistiColumn("A", lambda args: args[0].set_vika_texti(args[1]), lambda dto: dto.get_vika_texti())]

        for s in range(ord("B"), ord("G") + 1):
            col_stafur = chr(s)
            columns += [
                ThrifalistiColumn(col_stafur, lambda args: args[0].add_to_thrifalisti(args[1], args[2]),
                                  lambda args: args[0].get_thrif(args[1]), is_thrif=True)]
        return columns

    def __get_col_to_hus_map(self):
        if not self.__col_to_hus_map:
            self.__col_to_hus_map = {
                col.get_pos(): get_sheet_value(self._get_sheet(), col.get_pos(), self._get_info().get_lykill_row())
                for col in self._get_columns()}
        return self.__col_to_hus_map

    def write(self, entities):
        super().write(entities)  # todo filter is_fri

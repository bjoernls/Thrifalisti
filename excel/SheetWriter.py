from excel.Column import convert_to_num, Column
from excel.Utils import filter_cols_before_start
from excel.sheet_infos.YfirlitSheetInfo import YfirlitSheetInfo


class SheetWriter:

    def __init__(self, sheet, mapper, info, columns):
        self._sheet = sheet
        self._mapper = mapper
        self._info = info
        self._columns = columns

    def write(self, entities):
        row_no = self._info.get_start_write_row_col()[0]
        for dto in self._map_to_dtos(entities):
            filtered_cols = list(filter(lambda c: filter_cols_before_start(c, self._info), self._columns))
            for col in filtered_cols:
                self._set_sheet_value(row_no, col.get_pos(), self._get_write_value(dto, col))
            row_no += 1

    def _map_to_dtos(self, entities):
        raise NotImplementedError

    def _set_sheet_value(self, row, col, value):
        self._sheet.cell(row, convert_to_num(col)).value = value

    def _get_write_value(self, dto, col):
        raise NotImplementedError


class ThrifalistiSheetWriter(SheetWriter):

    def __init__(self, sheet, mapper, info, columns, col_to_hus_map):
        super().__init__(sheet, mapper, info, columns)
        self.__col_to_hus_map = col_to_hus_map

    def _map_to_dtos(self, thrifalisti):
        return [self._mapper.map_to_dto(thrifalisti.get_vikuthrifalisti(v.get_vika_nr()))
                for v in thrifalisti.get_vikuthrifalistar()]

    def _get_write_value(self, dto, col: Column):
        return col.getter(dto, self.__col_to_hus_map[col.get_pos()])


class YfirlitSheetWriter(SheetWriter):
    def _map_to_dtos(self, foreldralisti):
        if self._info.get_type() == YfirlitSheetInfo.Types.LS:
            foreldralisti = list(filter(lambda f: any(h.get_nafn() == "Leikskóli" for h in f.get_husalisti()), foreldralisti))
        foreldralisti.sort(key=lambda f: f.get_count(), reverse=True)
        return [self._mapper.map_to_dto(f) for f in foreldralisti]

    def _get_write_value(self, dto, col):
        return col.getter(dto)

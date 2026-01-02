from enum import Enum

from excel.sheet_infos.SheetInfo import SheetInfo


class YfirlitSheetInfo(SheetInfo):
    class Types(Enum):
        LS = 1,
        GS = 2

    def __init__(self, type: Types):
        self.__type = type

    def get_sheet_name(self):
        if self.__type == YfirlitSheetInfo.Types.GS:
            return "Yfirlit"
        if self.__type == YfirlitSheetInfo.Types.LS:
            return "Yfirlit - Ylur"

    def get_start_read_row_col(self):
        return [3, "A"]

    def get_start_write_row_col(self):
        return [3, "A"]

    def get_lykill_row(self):
        return 2

    def get_type(self):
        return self.__type

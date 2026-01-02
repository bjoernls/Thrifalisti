from excel.sheet_infos.SheetInfo import SheetInfo


class ThrifalistiSheetInfo(SheetInfo):
    def get_sheet_name(self):
        return "Þrifalisti"

    def get_start_read_row_col(self):
        return [3, "A"]

    def get_start_write_row_col(self):
        return [3, "B"]

    def get_lykill_row(self):
        return 2

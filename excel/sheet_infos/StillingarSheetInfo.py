from excel.sheet_infos.SheetInfo import SheetInfo


class StillingarSheetInfo(SheetInfo):

    def get_sheet_name(self):
        return "Stillingar"

    def get_start_read_row_col(self):
        return [2, "A"]

    def get_start_write_row_col(self):
        raise NotImplementedError
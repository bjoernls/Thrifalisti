from excel.sheet_infos.SheetInfo import SheetInfo


def convert_to_num(col):
    return ord(col.lower()) - 96


class Dto:
    def is_empty(self):
        raise NotImplementedError()

    def skip(self):
        return False


class Column:
    def __init__(self, pos, setter, getter):
        self.__pos = pos
        self.__setter = setter
        self.__getter = getter

    def getter(self):
        return self.__getter()

    def setter(self, val):
        self.__setter(val)

    def get_pos(self):
        return self.__pos

    def get_pos_num(self):
        return convert_to_num(self.get_pos())


class DtoIterator:

    def __init__(self, sheet, info: SheetInfo):
        self.sheet = sheet
        self.row = info.get_start_read_row_col()[0] - 1
        self.col = convert_to_num(info.get_start_read_row_col()[1])
        self.dto_factory = info.create_dto(sheet)

    def __iter__(self):
        return self

    def __next__(self):
        dto = self.__create_dto()
        while dto.skip():
            dto = self.__create_dto()

        if dto.is_empty():
            raise StopIteration
        return dto

    def __create_dto(self):
        self.row += 1
        return self.dto_factory(self.row)

    def get_value(self, col):
        return self.sheet.cell(self.row, col).value

    def get_dto(self):
        raise NotImplementedError("Please Implement this method")
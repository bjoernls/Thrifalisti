import openpyxl

from control.AlgorithmException import MaximumAllocationsExceededException, MinVikubilNotMetException, \
    AlgorithmException
from control.Thrifalisti import Thrifalisti
from control.ThrifalistiAlgo import ThrifalistiAlgo
from excel.SheetHandler import HusSheetHandler, ThrifalistiSheetHandler, ForeldriSheetHandler, YfirlitSheetHandler


def print_sorted_foreldralisti(foreldralisti):
    foreldralisti.sort(key=lambda foreldri: foreldri.get_vikubil())
    for f in foreldralisti:
        print(f)


def compute(wb):
    i = 0

    husalisti = __get_husalisti(wb)
    foreldralisti = __get_foreldralisti(husalisti, wb)
    thrifalisti = __get_thrifalisti(foreldralisti, husalisti, wb)

    while True:
        i += 1

        try:
            ThrifalistiAlgo(foreldralisti).compute(thrifalisti)
        except AlgorithmException as e:
            print(e.get_message())
            foreldralisti, thrifalisti = __reset_listar(husalisti, wb)
            continue

        min_vikubil = __calc_min_vikubil(foreldralisti)
        max_thrif_count = __calc_max_thrif_count(foreldralisti)
        print(f"min vikubil: {str(min_vikubil)}, max thrif count: {str(max_thrif_count)}")

        if min_vikubil >= 5 and max_thrif_count <= 3:
            break
        else:
            foreldralisti, thrifalisti = __reset_listar(husalisti, wb)

    print(str(i) + " runs")

    tl_handler = ThrifalistiSheetHandler(wb, husalisti, foreldralisti)
    y_handler = YfirlitSheetHandler(wb)
    write_to_excel_and_save(thrifalisti, foreldralisti, tl_handler, y_handler, wb)


def __reset_listar(husalisti, wb):
    foreldralisti = __get_foreldralisti(husalisti, wb)
    thrifalisti = __get_thrifalisti(foreldralisti, husalisti, wb)
    return foreldralisti, thrifalisti


def __get_thrifalisti(foreldralisti, husalisti, wb):
    thrifalisti = Thrifalisti(ThrifalistiSheetHandler(wb, husalisti, foreldralisti).read())
    return thrifalisti


def __get_foreldralisti(husalisti, wb):
    foreldralisti = ForeldriSheetHandler(wb, husalisti).read()
    return foreldralisti


def __get_husalisti(wb):
    husalisti = HusSheetHandler(wb).read()
    return husalisti


def __calc_min_vikubil(foreldralisti):
    return min([f.get_vikubil() for f in list(filter(lambda f: f.get_vikubil() > 0, foreldralisti))])


def __calc_max_thrif_count(foreldralisti):
    return max([f.get_count() for f in foreldralisti])


def write_to_excel_and_save(thrifalisti, foreldralisti, thrifalisti_sheet_handler, yfirlit_handler, wb):
    yfirlit_handler.write(foreldralisti)
    thrifalisti_sheet_handler.write(thrifalisti)
    wb.save("result.xlsx")


def calc_viku_fjoldi(vikuthrifalistar):
    return len(list(filter(lambda v: not v.is_fri(), vikuthrifalistar)))


if __name__ == '__main__':
    # compute(openpyxl.load_workbook("Testgögn.xlsx"))
    compute(openpyxl.load_workbook("Þrifalisti - Haust_2024.xlsx"))

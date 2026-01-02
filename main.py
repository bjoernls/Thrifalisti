import openpyxl

from control.AlgorithmException import AlgorithmException
from control.Thrifalisti import Thrifalisti
from control.ThrifalistiAlgo import ThrifalistiAlgo
from excel.SheetHandler import HusSheetHandler, ThrifalistiSheetHandler, ForeldriSheetHandler, YfirlitSheetHandler
import configparser

def print_sorted_foreldralisti(foreldralisti):
    foreldralisti.sort(key=lambda foreldri: foreldri.get_vikubil())
    for f in foreldralisti:
        print(f)


def compute(wb, algo_config):
    i = 0

    stillingar = __get_stillingar(wb)
    # TODO listahandler
    husalisti = __get_husalisti(wb)
    foreldralisti = __get_foreldralisti(husalisti, wb)
    thrifalisti = __get_thrifalisti(foreldralisti, husalisti, wb)
    res = False

    while not res:
        i += 1

        try:
            res = ThrifalistiAlgo(foreldralisti, algo_config).compute(thrifalisti)
        except AlgorithmException as e:
            print(e.get_message())
            foreldralisti, thrifalisti = __reset_listar(husalisti, wb)
            continue

        if not __verify_leikskoli(foreldralisti, husalisti, thrifalisti):
            foreldralisti, thrifalisti = __reset_listar(husalisti, wb)
            continue

        print(
            f"min vikubil: {str(__calc_min_vikubil(foreldralisti))}, max thrif count: {str(__calc_max_thrif_count(foreldralisti))}")



    print(str(i) + " runs")

    tl_handler = ThrifalistiSheetHandler(wb, husalisti, foreldralisti)
    y_handler = YfirlitSheetHandler(wb)
    write_to_excel_and_save(thrifalisti, foreldralisti, tl_handler, y_handler, wb)


def __verify_leikskoli(foreldralisti, husalisti, thrifalisti):
    res = True
    leikskoli = list(filter(lambda h: h.get_nafn() == "Leikskóli", husalisti))[0]
    foreldri_med_leikskola = []
    for t in thrifalisti.get_vikuthrifalistar():
        foreldri_med_leikskola += [t.get_foreldri_i_husi(leikskoli)]
    foreldrar_skrad_med_leikskola = list(filter(lambda f: leikskoli in f.get_husalisti(), foreldralisti))
    for f in foreldrar_skrad_med_leikskola:
        if not f in foreldri_med_leikskola:
            print(f"{f.get_nafn()} er ekki með skráð þrif í leikskóla")
            res = False
    return res


def __reset_listar(husalisti, wb):
    foreldralisti = __get_foreldralisti(husalisti, wb)
    thrifalisti = __get_thrifalisti(foreldralisti, husalisti, wb)
    return foreldralisti, thrifalisti


def __get_thrifalisti(foreldralisti, husalisti, wb):
    return Thrifalisti(ThrifalistiSheetHandler(wb, husalisti, foreldralisti).read())


def __get_foreldralisti(husalisti, wb):
    return ForeldriSheetHandler(wb, husalisti).read()


def __get_stillingar(wb):
    return StillingarSheetHandler(wb).read()


def __get_husalisti(wb):
    return HusSheetHandler(wb).read()


def __calc_min_vikubil(foreldralisti):
    return min([f.get_vikubil() for f in list(filter(lambda f: f.get_vikubil() > 0, foreldralisti))])


def __calc_max_thrif_count(foreldralisti):
    return max([f.get_count() for f in foreldralisti])


def write_to_excel_and_save(thrifalisti, foreldralisti, husalisti, wb):
    YfirlitSheetHandler(wb, YfirlitSheetInfo.Types.GS).write(foreldralisti)
    YfirlitSheetHandler(wb, YfirlitSheetInfo.Types.LS).write(foreldralisti)
    ThrifalistiSheetHandler(wb, husalisti, foreldralisti).write(thrifalisti)
    wb.save("result.xlsx")


def calc_viku_fjoldi(vikuthrifalistar):
    return len(list(filter(lambda v: not v.is_fri(), vikuthrifalistar)))


if __name__ == '__main__':
    # compute(openpyxl.load_workbook("Testgögn.xlsx"))
    config = configparser.ConfigParser()
    config.read('config.ini')
    compute(openpyxl.load_workbook("result 5.xlsx"), config['ALGO_PARAMS'])

class Stillingar:

    def __init__(self, dtos):
        self.__hamark_vikufjoldi = None
        self.__lagmark_vikubil = None
        __nafn_map = {
            "Hámark fjöldi þrifa": lambda x: self.__set_hamark_vikufjoldi(x),
            "Lágmark vikubil": lambda x: self.__set_lagmark_vikubil(x)
        }

        for dto in dtos:
            __nafn_map[dto.get_nafn()](dto.get_gildi())

    def __set_lagmark_vikubil(self, vikubil):
        self.__lagmark_vikubil = vikubil

    def __set_hamark_vikufjoldi(self, hamark):
        self.__hamark_vikufjoldi = hamark


    def get_hamark_vikufjoldi(self):
        return self.__hamark_vikufjoldi

    def get_lagmark_vikubil(self):
        return self.__lagmark_vikubil
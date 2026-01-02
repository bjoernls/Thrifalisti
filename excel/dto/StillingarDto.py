class StillingarDto:

    def __init__(self):
        self.__nafn = None
        self.__gildi = None

    def set_nafn(self, nafn):
        self.__nafn = nafn

    def set_gildi(self, gildi):
        self.__gildi = gildi

    def get_nafn(self):
        return self.__nafn

    def get_gildi(self):
        return self.__gildi

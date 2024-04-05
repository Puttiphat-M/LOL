import sys

from PySide6.QtWidgets import QApplication

from MachineEvent import MachineEvent
from UI.StartPage import StartPage
import UI.DepositPage as DepositPage
import UI.DonePage as DonePage
import UI.DonatePage as DonatePage
from QRGenerator import QRGenerator
from PySide6.QtCore import QObject, Signal
import Encrypt as encrypt


class LotusSystem(QObject):
    bottleChanged = Signal(int)

    def __init__(self):
        super().__init__()
        self.bottle = 0
        self.page = None
        # self.machine_event = MachineEvent(self)

        # if LotusSystem.__instance is not None:
        #     raise Exception("This class is a singleton!")
        # else:
        #     LotusSystem.__instance = self
        #     self.__current = None

    def start(self):
        self.page = "StartPage"
        self.__current = StartPage(self)

    def setPage(self,page):
        self.page = page
        if self.__current is not None:
            self.__current.close()  # Close the old page
        self.changePage()
        if page == "StartPage":
            self.bottle = 0

    def changePage(self):
        if self.page == "StartPage":
            self.__current = StartPage(self)
        elif self.page == "DepositPage":
            self.__current = DepositPage.DepositPage(self)
            # self.machine_event.turn_on()
        elif self.page == "DonePage":
            self.__current = DonePage.DonePage(self)
        elif self.page == "DonatePage":
            self.__current = DonatePage.DonatePage(self)
        else:
            self.__current = None

    # @staticmethod
    # def getInstance():
    #     if LotusSystem.__instance is None:
    #         LotusSystem()
    #     return LotusSystem.__instance

    def getQR(self):
        encryptBottle = encrypt.Encrypt().encrypt(str(self.bottle))
        QRGenerator.generateQR(encryptBottle)
        return QRGenerator.generateQR

    def increment_bottle(self):
        self.bottle += 1
        self.bottleChanged.emit(self.bottle)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    lotus_system = LotusSystem()
    lotus_system.start()
    sys.exit(app.exec())

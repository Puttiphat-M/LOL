import sys
import threading

import serial
from PySide6.QtWidgets import QApplication

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
        # check if LotusSystem is already created
        super().__init__()
        self.bottle = 0
        self.page = None
        # self.port_name = 'COM5'
        # self.ser = serial.Serial(self.port_name, 9600)

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
        self.changePage()
        if page == "StartPage":  # Check if the page is not DepositPage
            self.bottle = 0

    def changePage(self):
        if self.page == "StartPage":
            self.__current = StartPage(self)
        elif self.page == "DepositPage":
            self.__current = DepositPage.DepositPage(self)
            threading.Thread(target=self.get_user_input).start()
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
        ecryptBottle = encrypt.Encrypt().encrypt(str(self.bottle))
        # QRGenerator.generateQR(encryptBottle)
        return QRGenerator.generateQR

    def set_bottle(self, bottle):
        self.bottle = bottle
        self.bottleChanged.emit(bottle)

    def get_user_input(self):
        while self.page == "DepositPage":
            user_input = input("Enter value: ")
            if user_input.lower() == "exit":
                break
            try:
                new_value = int(user_input)
                self.set_bottle(new_value)
            except ValueError:
                print("Invalid input. Please enter an integer value.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    lotus_system = LotusSystem()
    lotus_system.start()
    sys.exit(app.exec())

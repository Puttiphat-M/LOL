from UI.Component import load_fonts
from UI.StartPage import StartPage
import UI.DepositPage as DepositPage
import UI.DonePage as DonePage
import UI.DonatePage as DonatePage
from System.QRGenerator import QRGenerator
from PySide6.QtCore import QObject, Signal


class LotusSystem(QObject):
    machine_event = None
    bottle_changed = Signal(int)
    __instance = None
    page = None
    bottle = 0

    def __init__(self):
        super().__init__()
        if LotusSystem.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            LotusSystem.__instance = self
            self.__current = None
            if LotusSystem.machine_event is None:
                from System.MachineEvent import MachineEvent
                LotusSystem.machine_event = MachineEvent()

    @staticmethod
    def get_instance():
        if LotusSystem.__instance is None:
            LotusSystem()
        return LotusSystem.__instance

    @staticmethod
    def start():
        load_fonts()
        LotusSystem.page = "StartPage"
        LotusSystem.__current = StartPage()

    @staticmethod
    def set_page(page):
        LotusSystem.page = page
        LotusSystem.change_page()
        if page == "StartPage":
            LotusSystem.bottle = 0

    @staticmethod
    def change_page():
        if LotusSystem.page == "StartPage":
            LotusSystem.__current = StartPage()
        elif LotusSystem.page == "DepositPage":
            LotusSystem.__current = DepositPage.DepositPage()
            LotusSystem.machine_event.turn_on()
        elif LotusSystem.page == "DonePage":
            LotusSystem.machine_event.pause()
            LotusSystem.__current = DonePage.DonePage()
        elif LotusSystem.page == "DonatePage":
            LotusSystem.machine_event.pause()
            LotusSystem.__current = DonatePage.DonatePage()
        else:
            LotusSystem.__current = None

    @staticmethod
    def get_qr():
        qr_image = QRGenerator().generate_qr(LotusSystem.bottle)
        return qr_image

    @staticmethod
    def increment_bottle():
        LotusSystem.bottle += 1
        LotusSystem.get_instance().bottle_changed.emit(LotusSystem.bottle)
        if LotusSystem.bottle == 10:
            LotusSystem.machine_event.pause()

    @staticmethod
    def get_bottle_count():
        return LotusSystem.bottle

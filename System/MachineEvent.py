import serial
import serial.tools.list_ports
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QApplication, QSizePolicy


def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    keywords = ["Arduino", "USB", "Serial"]
    for port in ports:
        if any(keyword in port.description for keyword in keywords):
            return port.device
    return None


class CustomAlert(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Alert")
        self.setStyleSheet("background-color: white;")

        # Layout setup
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Message label setup
        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("color: rgb(0, 0, 0);")
        self.message_label.setFont(QFont("Lotuss Smart HL", int(self.width() / 13)))  # Font size relative to dialog height
        layout.addWidget(self.message_label)

        # Ok button setup
        ok_button = QPushButton("ตกลง")
        ok_button.setFixedSize(int(self.width() / 2), int(self.width() / 8))  # Fixed height, expanding width
        ok_button.setStyleSheet('''
            QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(1, 187, 181);
                border: 2px solid rgb(0, 0, 0);  /* Add a border for better visibility */
                border-radius: 15px;  /* Increased border radius */
                font-family: "Lotuss Smart HL";
                font-size: 20px;
                padding: 10px 20px;  /* Increased padding for a larger button */
            }
            QPushButton:pressed {
                background-color: rgb(0, 150, 145);
            }
        ''')
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignCenter)

        # Adding margins and spacing
        layout.setContentsMargins(int(self.width() / 10), int(self.height() / 10),
                                  int(self.width() / 10), int(self.height() / 10))
        layout.setSpacing(int(self.height() / 20))

        # Set the size of the dialog to be a percentage of the screen size
        screen_size = QApplication.primaryScreen().size()
        self.setFixedSize(screen_size.width() * 0.4, screen_size.height() * 0.3)


class ResetAlert(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Alert")
        self.setStyleSheet("background-color: white;")

        # Layout setup
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Message label setup
        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("color: rgb(0, 0, 0);")
        self.message_label.setFont(QFont("Lotuss Smart HL", int(self.width() / 15)))  # Font size relative to dialog height
        layout.addWidget(self.message_label)

        # Ok button setup
        ok_button = QPushButton("ตกลง")
        ok_button.setFixedSize(int(self.width() / 2), int(self.width() / 8))  # Fixed height, expanding width
        ok_button.setStyleSheet('''
            QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(1, 187, 181);
                border: 2px solid rgb(0, 0, 0);  /* Add a border for better visibility */
                border-radius: 10px;  /* Increased border radius */
                font-family: "Lotuss Smart HL";
                font-size: 20px;
                padding: 10px 20px;  /* Increased padding for a larger button */
            }
            QPushButton:pressed {
                background-color: rgb(0, 150, 145);
            }
        ''')
        ok_button.clicked.connect(self.back_to_start_page)
        layout.addWidget(ok_button, alignment=Qt.AlignCenter)

        # Adding margins and spacing
        layout.setContentsMargins(int(self.width() / 10), int(self.height() / 10),
                                  int(self.width() / 10), int(self.height() / 10))
        layout.setSpacing(int(self.height() / 20))

        # Set the size of the dialog to be a percentage of the screen size
        screen_size = QApplication.primaryScreen().size()
        self.setFixedSize(screen_size.width() * 0.4, screen_size.height() * 0.3)

    def back_to_start_page(self):
        from LotusSystem import LotusSystem
        self.close()
        LotusSystem.set_page("StartPage")


class MachineEvent:
    def __init__(self):

        self.port_name = find_arduino_port()

        print(self.port_name)
        if self.port_name is None:
            raise Exception("No Arduino found")
        else:
            self.ser = serial.Serial(self.port_name, 9600)

        self.timer = QTimer()
        self.timer.timeout.connect(self.read_from_arduino)
        self.timer.start(100)

        self.notification_dialog = None

    def turn_on(self):
        self.send_command(b'1')

    def pause(self):
        self.send_command(b'0')

    def send_command(self, command):
        self.ser.write(command)

    def read_from_arduino(self):
        from LotusSystem import LotusSystem
        if self.ser.in_waiting > 0:
            message = self.ser.readline().decode('utf-8').strip()

            print(message)
            if LotusSystem.bottle < 10:
                if message == "h":
                    if self.notification_dialog and self.notification_dialog.isVisible():
                        self.notification_dialog.close()
                    LotusSystem.increment_bottle()

                elif message == "n":
                    if LotusSystem.page == "DepositPage":
                        self.show_notification("กรุณาหยอดขวด")

            if message == "s":
                self.pause()
                if self.notification_dialog and self.notification_dialog.isVisible():
                    self.notification_dialog.close()
                if LotusSystem.bottle > 0:
                    LotusSystem.set_page("DonatePage")
                else:
                    LotusSystem.set_page("StartPage")

            elif message == "f":
                self.pause()
                self.show_reset_notification("ขออภัยขณะนี้ที่บรรจุขวดเต็ม กรุณาติดต่อพนักงาน")

    def show_notification(self, message):
        self.notification_dialog = CustomAlert(message)
        self.notification_dialog.setWindowFlags(self.notification_dialog.windowFlags() | Qt.WindowStaysOnTopHint)
        self.notification_dialog.show()

    def show_reset_notification(self, message):
        self.notification_dialog = ResetAlert(message)
        self.notification_dialog.setWindowFlags(self.notification_dialog.windowFlags() | Qt.WindowStaysOnTopHint)
        self.notification_dialog.show()




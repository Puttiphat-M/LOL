import serial
import serial.tools.list_ports
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

def find_arduino_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"Port: {port.device}, Description: {port.description}")
        return port.device
    return None


class CustomAlert(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Alert")
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()
        self.setFixedSize(300, 150)
        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("color: rgb(0, 0, 0);")
        self.message_label.setFont(QFont("Lotuss Smart HL", 18))
        layout.addWidget(self.message_label)
        ok_button = QPushButton("ตกลง")
        ok_button.setStyleSheet('''
            QPushButton {
                color: rgb(0, 0, 0);
                background-color: rgb(1, 187, 181);
                border-radius: 25px;
                font-family: "Lotuss Smart HL";
                font-size: 15px;
                
            }
        ''')
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)
        self.setLayout(layout)


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

    def show_notification(self, message):
        self.notification_dialog = CustomAlert(message)
        self.notification_dialog.setWindowFlags(self.notification_dialog.windowFlags() | Qt.WindowStaysOnTopHint)
        self.notification_dialog.show()
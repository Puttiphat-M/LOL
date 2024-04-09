import serial
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton


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
        ok_button = QPushButton("OK")
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
    def __init__(self, master):
        self.port_name = '/dev/cu.usbmodem1201'
        self.master = master
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
        if self.ser.in_waiting > 0:
            message = self.ser.readline().decode('utf-8').strip()
            if self.master.bottle < 10:
                if message == "has bottle":
                    if self.notification_dialog and self.notification_dialog.isVisible():
                        self.notification_dialog.close()
                    print("bottle +1")
                    self.master.increment_bottle()

                elif message == "No bottle":
                    if self.master.__current is "DepositPage":
                        self.show_notification("Please insert a bottle.")
                    print("No bottle")

            if message == "stop Program":
                self.pause()
                if self.notification_dialog and self.notification_dialog.isVisible():
                    self.notification_dialog.close()
                self.master.set_page("StartPage")
                print("stop Program")

    def show_notification(self, message):
        self.notification_dialog = CustomAlert(message)
        self.notification_dialog.setWindowFlags(self.notification_dialog.windowFlags() | Qt.WindowStaysOnTopHint)
        self.notification_dialog.show()

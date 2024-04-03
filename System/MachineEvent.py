import serial
from PySide6.QtCore import QTimer


class MachineEvent:
    def __init__(self, master):
        self.port_name = '/dev/cu.usbmodem1201'
        self.master = master
        self.ser = serial.Serial(self.port_name, 9600)

    def turn_on(self):
        self.send_command(b'1')

    def send_command(self, command):
        self.ser.write(command)
        self.read_from_arduino()

    def read_from_arduino(self):
        if self.ser.in_waiting > 0:
            message = self.ser.readline().decode('utf-8').strip()

            if message == "has bottle":

                print("bottle +1")
                self.master.increment_bottle()

            elif message == "No bottle":

                print("Timeout")

            else:
                # Handle other messages
                print("Received unexpected message:", message)
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_from_arduino)
        self.timer.start(100)

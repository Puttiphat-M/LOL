import os
import sys
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap, QPainter, QFont


class DonatePage(QWidget):
    def __init__(self, lotus_system):
        super().__init__()
        self.timeout_count = 5
        self.lotus_system = lotus_system
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Load background image
        self.background_pixmap = QPixmap(os.path.join(script_dir, u"../resources/LotusBackground.jpg"))

        thankyou_label1 = QLabel("ขอขอบคุณ")
        thankyou_label1.setFont(QFont("Lotuss Smart HL", 65, QFont.Bold))
        thankyou_label1.setStyleSheet("color: rgb(1, 187, 181);")
        thankyou_label1.setAlignment(Qt.AlignCenter)

        thankyou_label2 = QLabel("สำหรับการบริจาค")
        thankyou_label2.setFont(QFont("Lotuss Smart HL", 65, QFont.Bold))
        thankyou_label2.setStyleSheet("color: rgb(1, 187, 181);")
        thankyou_label2.setAlignment(Qt.AlignCenter)

        self.logo_label_footer = QLabel()
        logo_pixmap = QPixmap(os.path.join(script_dir, u"../resources/LogoLotus 100x30.png"))
        self.logo_label_footer.setPixmap(logo_pixmap)
        self.logo_label_footer.setStyleSheet("background-color: transparent;")

        thankyou_layout = QVBoxLayout()
        thankyou_layout.addWidget(thankyou_label1)
        thankyou_layout.addWidget(thankyou_label2)

        footer_layout = QHBoxLayout()
        footer_layout.addStretch(1)
        footer_layout.addWidget(self.logo_label_footer)

        widget = QWidget()  # Create a widget to contain the layout
        widget.setLayout(thankyou_layout)  # Set the layout to the widget
        widget.setStyleSheet("background-color: white;")  # Set the background color of the widget

        main_layout = QVBoxLayout(self)
        main_layout.addSpacing(62)
        main_layout.addWidget(widget)
        main_layout.addStretch(1)
        main_layout.addLayout(footer_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.reset)
        self.timer.start(1000)  # Update timer label every second

        # Set window title and geometry
        self.setWindowTitle("Donate Page")
        self.setStyleSheet("background-color: white;")
        self.setFixedSize(640, 480)
        self.update_background()
        self.show()

    def update_background(self):
        # Scale the background image to fit the current size of the widget
        self.background_pixmap = self.background_pixmap.scaled(self.width(), self.height() - (self.height() / 7))

    def reset(self):
        self.timeout_count -= 1  # Decrease timeout count by 1
        if self.timeout_count <= 0:
            self.lotus_system.setPage("StartPage")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.background_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = DonatePage()
    sys.exit(app.exec())

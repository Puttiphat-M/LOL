import os
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap, QPainter, QFont


class StartPage(QWidget):
    def __init__(self, lotus_system):
        super().__init__()
        self.lotus_system = lotus_system
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Load background image
        self.background_pixmap = QPixmap(os.path.join(script_dir, u"../resources/LotusBackground.jpg"))

        # Create the bottle logo
        self.logo_label = QLabel()
        self.logo_label.setStyleSheet("background-color: transparent;")
        logo_pixmap = QPixmap(os.path.join(script_dir, u"../resources/EggLogo.png"))
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)

        # Create "begin" button
        begin_button = QPushButton("เริ่มต้นใช้งาน")
        begin_button.setFont(QFont("Lotuss Smart HL", 22, QFont.Bold))
        begin_button.setFixedSize(260, 52)
        begin_button.setStyleSheet('''
            QPushButton {
                color: rgb(255, 255, 255);
                background-color: rgb(255, 196, 0);
                border-radius: 25px;
            }
        ''')
        begin_button.clicked.connect(self.deposit)

        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(begin_button)
        button_layout.addStretch(1)

        footer_label = QLabel("*กรุณาแอดไลน์ Lotus’s ก่อนทำการใช้งาน")
        footer_label.setFont(QFont("Lotuss Smart HL", 19))
        footer_label.setStyleSheet('''
                    QLabel {
                        color: rgb(216, 7, 5);
                        background-color: transparent;
                    }
                ''')

        self.logo_label_footer = QLabel()
        logo_pixmap = QPixmap(os.path.join(script_dir, u"../resources/LogoLotus 100x30.png"))
        self.logo_label_footer.setPixmap(logo_pixmap)
        self.logo_label_footer.setStyleSheet("background-color: transparent;")

        footer_layout = QHBoxLayout()
        footer_layout.addWidget(footer_label)
        footer_layout.addStretch(1)
        footer_layout.addWidget(self.logo_label_footer)

        main_layout = QVBoxLayout(self)
        main_layout.addStretch(1)
        main_layout.addWidget(self.logo_label)
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(footer_layout)

        # Set window title and geometry
        self.setWindowTitle("Start Page")
        self.setStyleSheet("background-color: white;")
        self.setFixedSize(640, 480)
        self.update_background()
        self.show()

    def deposit(self):
        self.lotus_system.setPage("DepositPage")

    def update_background(self):
        # Scale the background image to fit the current size of the widget
        self.background_pixmap = self.background_pixmap.scaled(self.width(), self.height() - (self.height() / 7))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.background_pixmap)

    # def resizeEvent(self, event):
    #     self.update_background()
    #     self.repaint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = StartPage()
    sys.exit(app.exec())

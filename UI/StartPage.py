import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PySide6.QtGui import QPixmap, QPainter, QFont


class StartPage(QWidget):
    def __init__(self):
        super().__init__()
        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.background_pixmap = QPixmap(os.path.join(script_dir, u"../resources/LotusBackground.jpg"))

        self.logo_label = QLabel()
        self.logo_label.setStyleSheet("background-color: transparent;")
        logo_pixmap = QPixmap(os.path.join(script_dir, u"../resources/EggLogo.png"))
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)

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
        begin_button.clicked.connect(self.go_to_deposit_page)

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

        self.setWindowTitle("Start Page")
        self.setStyleSheet("background-color: white;")
        self.setFixedSize(640, 480)
        self.update_background()
        self.show()

    def update_background(self):
        self.background_pixmap = self.background_pixmap.scaled(self.width(), self.height() - (self.height() / 7))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.background_pixmap)

    def go_to_deposit_page(self):
        from System.LotusSystem import LotusSystem
        LotusSystem.set_page("DepositPage")
        self.close()

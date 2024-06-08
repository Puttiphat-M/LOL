from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QApplication
from PySide6.QtGui import QFont, QPixmap, QPainter


class StartPage(QWidget):
    def __init__(self):
        super().__init__()
        self.background_pixmap = None
        self.set_full_screen()
        self.logo_label = QLabel()
        self.logo_label.setStyleSheet("background-color: transparent;")
        from UI.Component import resource_path
        self.logo_pixmap = QPixmap(resource_path("resources/EggLogo.png"))
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)

        self.begin_button = QPushButton("เริ่มต้นใช้งาน")
        self.begin_button.setFont(QFont("Lotuss Smart HL", 22, QFont.Bold))
        self.begin_button.setMinimumSize(260, 52)
        self.begin_button.setStyleSheet('''
            QPushButton {
                color: rgb(255, 255, 255);
                background-color: rgb(255, 196, 0);
                border-radius: 25px;
            }
        ''')
        self.begin_button.clicked.connect(self.go_to_deposit_page)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.begin_button)
        button_layout.addStretch(1)

        self.footer_label = QLabel("*กรุณาแอดไลน์ Lotus’s ก่อนทำการใช้งาน")
        self.footer_label.setFont(QFont("Lotuss Smart HL", 19))
        self.footer_label.setStyleSheet('''
            QLabel {
                color: rgb(216, 7, 5);
                background-color: transparent;
            }
        ''')

        self.logo_label_footer = QLabel()
        self.lotus_logo_pixmap = QPixmap(resource_path("resources/Lotus.png"))
        self.logo_label_footer.setPixmap(self.lotus_logo_pixmap)
        self.logo_label_footer.setStyleSheet("background-color: transparent;")

        footer_layout = QHBoxLayout()
        footer_layout.addWidget(self.footer_label)
        footer_layout.addStretch(1)
        footer_layout.addWidget(self.logo_label_footer)

        self.footer_container = QWidget()
        self.footer_container.setLayout(footer_layout)
        self.footer_container.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout(self)
        main_layout.addStretch(1)
        main_layout.addWidget(self.logo_label)
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout)
        main_layout.addStretch(2)
        main_layout.addWidget(self.footer_container)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setWindowTitle("Start Page")
        self.setStyleSheet("background-color: white;")
        self.setMinimumSize(640, 500)
        self.show()

    def paintEvent(self, event):
        from UI.Component import resource_path
        painter = QPainter(self)
        painter.drawPixmap(0, 0, QPixmap(resource_path("resources/LotusBackground.jpg")).scaled(self.width(), self.height()))
        painter.end()

    def set_full_screen(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateUI()

    def updateUI(self):
        button_width = int(self.width() * 0.25)
        button_height = int(self.height() * 0.1)
        self.begin_button.setFixedSize(button_width, button_height)
        self.begin_button.setFont(QFont("Lotuss Smart HL", int((self.width() + self.height()) / 55), QFont.Bold))
        self.footer_label.setFont(QFont("Lotuss Smart HL", int((self.width() + self.height()) / 70)))
        self.logo_label.setPixmap(self.logo_pixmap.scaled(self.width() / 2.15, self.height() / 2.2, Qt.KeepAspectRatio))
        self.logo_label_footer.setPixmap(self.lotus_logo_pixmap.scaled(self.width() / 6.4, self.height() / 15, Qt.KeepAspectRatio))

    def go_to_deposit_page(self):
        from LotusSystem import LotusSystem
        LotusSystem.set_page("DepositPage")
        self.close()

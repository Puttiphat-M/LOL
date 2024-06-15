import sys
from PySide6.QtWidgets import QApplication
from LotusSystem import LotusSystem


def main():
    app = QApplication([])
    lotus_system = LotusSystem.get_instance()
    lotus_system.start()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
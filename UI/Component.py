import os
import sys
from PySide6.QtGui import QFontDatabase


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    path = os.path.join(base_path, relative_path)
    return path


def load_fonts():
    font_paths = [
        'Font/LotussSmartHL-Bold.ttf',
        'Font/LotussSmartHL-ExtraBold.ttf',
        'Font/LotussSmartHL-Light.ttf',
        'Font/LotussSmartHL-Medium.ttf',
        'Font/LotussSmartHL-Regular.ttf'
    ]

    # List of font families to check
    font_families = [
        'Lotuss Smart HL'
    ]

    # Get the current list of available fonts
    available_fonts = QFontDatabase.families()

    for font_family in font_families:
        if font_family in available_fonts:
            print(f"Font {font_family} is already available.")
        else:
            print(f"Font {font_family} is not available, loading from file.")
            for font_path in font_paths:
                resolved_font_path = resource_path(font_path)
                font_id = QFontDatabase.addApplicationFont(str(resolved_font_path))
                if font_id == -1:
                    print(f"Failed to load font: {resolved_font_path}")
                else:
                    print(f"Successfully loaded font: {resolved_font_path}")

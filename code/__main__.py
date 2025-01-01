from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtWidgets import QApplication
from go import Go
import sys
import os


def customFont():
    # Get the current working directory and construct the font path
    current_dir = os.getcwd()
    font_path = os.path.join(current_dir, "assets/fonts/YsabeauSC-SemiBold.ttf")

    # Load custom font
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        return font_family
    else:
        font_family = "Helvetica"
        return font_family

def main():
    app = QApplication(sys.argv)
    font = QFont(customFont(), 14)
    app.setFont(font)
    myGo = Go()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()


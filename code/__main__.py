from PyQt6.QtWidgets import QApplication
from go import Go
import sys

def main():
    app = QApplication(sys.argv)
    myGo = Go()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QDockWidget, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from board import Board
from score_board import ScoreBoard
from game_logic import game_logic

class Go(QMainWindow):
    def __init__(self):
        super().__init__()
        self.createMenuBar()
        self.game_logic = game_logic()  # Create game logic instance
        self.initUI()

    def createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setNativeMenuBar(False)
        menuBar.setStyleSheet("""
            QMenuBar {
                background-color: #2d2d2d;
                color: white;
                font-family: 'YsabeauSC-SemiBold';
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
            QMenuBar::item:selected {
                background-color: #4a4a4a;
            }
            QMenu {
                background-color: #2d2d2d;
                color: white;
                font-family: 'YsabeauSC-SemiBold';
                border: 1px solid #3a3a3a;
            }
            QMenu::item:selected {
                background-color: #4a4a4a;
            }
        """)

        fileMenu = menuBar.addMenu("File")
        exitAction = fileMenu.addAction("Exit")
        exitAction.triggered.connect(self.close)
            
        helpMenu = menuBar.addMenu("Help")
        rulesAction = helpMenu.addAction("Rules")
        rulesAction.triggered.connect(self.showRules)
        aboutAction = helpMenu.addAction("About")
        aboutAction.triggered.connect(self.showAbout)

    def showRules(self):
        QMessageBox.information(self, "Go Rules", 
            "Basic rules:\n- Players alternate placing stones\n- Capture by surrounding\n- Control territory to win")

    def showAbout(self):
        QMessageBox.about(self, "About Go", "Go Game\nVersion 1.0")

# Call createMenuBar() in __init__() after super().__init__()

    def initUI(self):
        self.setStyleSheet("background-color: #1a1a1a;")
        
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        
        self.board = Board(self, self.game_logic)  # Pass game_logic instance
        self.board.setFixedSize(700,700)
        layout.addWidget(self.board)
        
        self.setCentralWidget(central_widget)
        
        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)

        self.resize(800, 750)
        self.center()
        self.setWindowTitle('Go')
        self.setStyleSheet("""
            QWidget#centralWidget {
                font-family: 'YsabeauSC-SemiBold';
            }
            """)
        self.show()
    

    def showRules(self):
        rules_text = """
        Basic Rules of Go:
        
        1. Players take turns placing stones
        2. Black plays first
        3. Capture stones by surrounding them
        4. Control territory to win
        5. Game ends when both players pass
        """
        QMessageBox.information(self, "Go Rules", rules_text)

    def showAbout(self):
        about_text = """
        Go Game
        Version 1.0
        
        A traditional board game with
        history spanning over 2,500 years.
        """
        QMessageBox.about(self, "About Go", about_text)

    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
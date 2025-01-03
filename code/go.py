from PyQt6.QtGui import QKeySequence

from pages.welcome_page import WelcomePage
from PyQt6.QtWidgets import QApplication, QScrollArea, QMessageBox, QMainWindow, QDockWidget, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from board import Board
from score_board import ScoreBoard
from game_logic import game_logic


class Go(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initWelcome()
        self.createMenuBar()
        self.game_logic = game_logic()  # Create game logic instance

    def initWelcome(self):
        self.welcome = WelcomePage(self)
        self.setCentralWidget(self.welcome)
        self.resize(800, 700)
        self.center()
        self.setWindowTitle('Go')
        self.show()

    def startGame(self):
        # When start game is clicked, initialize the game UI
        self.game_logic = game_logic()  # Reset game logic
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
        exitAction.setShortcut(QKeySequence("ctrl+q"))
        backToMenuAction = fileMenu.addAction("Back to Menu")
        backToMenuAction.triggered.connect(self.showWelcome)
        backToMenuAction.setShortcut(QKeySequence("ctrl+w"))
        fileMenu.addSeparator()  # separator line

        actionMenu = menuBar.addMenu("Actions")
        undoAction = actionMenu.addAction("Undo")
        undoAction.triggered.connect(lambda: self.scoreBoard.undoMove() if hasattr(self, 'scoreBoard') else None)
        undoAction.setShortcut(QKeySequence("Ctrl+Z"))
        resetAction = actionMenu.addAction("Reset Board")
        resetAction.setShortcut(QKeySequence("Ctrl+Shift+R"))
        resetAction.triggered.connect(lambda: self.scoreBoard.clearBoard() if hasattr(self, 'scoreBoard') else None)

        helpMenu = menuBar.addMenu("Help")
        rulesAction = helpMenu.addAction("Rules")
        rulesAction.setShortcut(QKeySequence("alt+h"))
        rulesAction.triggered.connect(self.showRules)
        aboutAction = helpMenu.addAction("About")
        aboutAction.setShortcut(QKeySequence("alt+i"))
        aboutAction.triggered.connect(self.showAbout)

    def showRules(self):
        QMessageBox.information(self, "Go Rules",
                                "Basic rules:\n- Players alternate placing stones\n- Capture by surrounding\n- Control territory to win")

    def showAbout(self):
        QMessageBox.about(self, "About Go", "Go Game\nVersion 1.0")

    def initUI(self):
        self.setStyleSheet("background-color: #1a1a1a;")

        # Create main widget
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #1a1a1a;
            }
            QScrollBar:vertical, QScrollBar:horizontal {
                background: #2d2d2d;
                width: 12px;
                height: 12px;
            }
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background: #4a4a4a;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
                background: #5a5a5a;
            }
        """)
        # Create content widget for scroll area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(40, 40, 40, 40)

        self.board = Board(self, self.game_logic)  # Pass game_logic instance
        self.board.setFixedSize(600, 600)
        content_layout.addWidget(self.board, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Set the widget in scroll area
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        # Set main widget as central widget
        self.setCentralWidget(main_widget)

        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)

        # Window setup
        self.resize(1000, 800)
        self.center()
        self.setWindowTitle('Go')
        self.show()

        def startGame(self):
            self.initUI()

    def showWelcome(self):
        # Remove scoreboard if it exists
        if hasattr(self, 'scoreBoard'):
            self.removeDockWidget(self.scoreBoard)
        # Show welcome page
        welcome = WelcomePage(self)
        self.setCentralWidget(welcome)

    def switchToTutorial(self, tutorial):
        self.setCentralWidget(tutorial)

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
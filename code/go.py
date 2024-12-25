from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from board import Board
from score_board import ScoreBoard
from game_logic import game_logic

class Go(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game_logic = game_logic()  # Create game logic instance
        self.initUI()

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
        self.show()

    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
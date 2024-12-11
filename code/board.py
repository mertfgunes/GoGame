from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush


class Board(QFrame):
    updatePrisonersSignal = pyqtSignal(int, int)
    updateTurnSignal = pyqtSignal(str)

    def __init__(self, parent, game_logic):
        super().__init__(parent)
        self.game_logic = game_logic
        self.initBoard()

    def initBoard(self):
        self.setStyleSheet("background-color: #92400E; border-radius: 8px;")
        self.setMinimumSize(600, 600)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.drawGrid(painter)
        self.drawStones(painter)

    def drawGrid(self, painter):
        painter.setPen(QPen(QColor(255, 255, 255, 50), 1))
        rect = self.contentsRect()
        cell_size = min(rect.width(), rect.height()) / 7

        # Draw lines
        for i in range(7):
            x = rect.left() + i * cell_size + cell_size / 2
            y = rect.top() + i * cell_size + cell_size / 2
            painter.drawLine(int(x), int(rect.top() + cell_size / 2),
                             int(x), int(rect.bottom() - cell_size / 2))
            painter.drawLine(int(rect.left() + cell_size / 2), int(y),
                             int(rect.right() - cell_size / 2), int(y))

    def drawStones(self, painter):
        rect = self.contentsRect()
        cell_size = min(rect.width(), rect.height()) / 7

        for row in range(7):
            for col in range(7):
                if self.game_logic.board[row][col] != 0:
                    x = rect.left() + col * cell_size + cell_size / 2
                    y = rect.top() + row * cell_size + cell_size / 2
                    color = Qt.GlobalColor.black if self.game_logic.board[row][col] == 1 else Qt.GlobalColor.white
                    painter.setBrush(QBrush(color))
                    painter.setPen(QPen(Qt.GlobalColor.black))
                    painter.drawEllipse(int(x - cell_size / 3), int(y - cell_size / 3),
                                        int(cell_size * 2 / 3), int(cell_size * 2 / 3))

    def mousePressEvent(self, event):
        rect = self.contentsRect()
        cell_size = min(rect.width(), rect.height()) / 7
        col = int((event.pos().x() - rect.left() - cell_size / 2) / cell_size)
        row = int((event.pos().y() - rect.top() - cell_size / 2) / cell_size)

        if 0 <= row < 7 and 0 <= col < 7:
            if self.game_logic.place_stone(row, col):
                self.update()

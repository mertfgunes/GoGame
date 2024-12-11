from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, pyqtSignal, QRect
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush


class Board(QFrame):
    updatePrisonersSignal = pyqtSignal(int, int)
    updateTurnSignal = pyqtSignal(str)

    def __init__(self, parent, game_logic):
        super().__init__(parent)
        self.game_logic = game_logic
        self.initBoard()

    def initBoard(self):
        '''Initialize the board with a default style and size.'''
        self.setStyleSheet("background-color: #92400E; border-radius: 8px;")
        self.setMinimumSize(600, 600)  # Ensure the widget has a minimum size

    def resizeEvent(self, event):
        '''Triggered whenever the widget is resized.'''
        super().resizeEvent(event)
        self.update()  # Redraw the board to adapt to the new size

    def paintEvent(self, event):
        '''Paint the board with a fixed square grid centered in the widget.'''
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Get the widget's dimensions
        widget_width = self.width()
        widget_height = self.height()
        grid_size = min(widget_width, widget_height)  # Square grid size
        margin_x = (widget_width - grid_size) // 2
        margin_y = (widget_height - grid_size) // 2

        # Create a square rect for the grid area
        self.grid_rect = QRect(margin_x, margin_y, grid_size, grid_size)

        # Draw grid and stones within the grid rect
        self.drawGrid(painter)
        self.drawStones(painter)

    def drawGrid(self, painter):
        '''Draws the grid inside the fixed square area.'''
        painter.setPen(QPen(QColor(255, 255, 255, 50), 3))
        grid_size = self.grid_rect.width()  # Square dimensions
        cell_size = grid_size / 7  # Divide the square into 7 cells

        # Draw vertical lines
        for i in range(8):  # From 0 to 7 inclusive (8 lines)
            x = self.grid_rect.left() + i * cell_size
            painter.drawLine(int(x), self.grid_rect.top(), int(x), self.grid_rect.bottom())

        # Draw horizontal lines
        for i in range(8):  # From 0 to 7 inclusive (8 lines)
            y = self.grid_rect.top() + i * cell_size
            painter.drawLine(self.grid_rect.left(), int(y), self.grid_rect.right(), int(y))

    def drawStones(self, painter):
        '''Draw stones (pieces) on the board.'''
        rect = self.contentsRect()  # Get the drawable area
        cell_size = min(rect.width(), rect.height()) / 7  # Ensure square cells

        for row in range(7):
            for col in range(7):
                if self.game_logic.board[row][col] != 0:  # Check if a stone exists
                    # Calculate the center of the cell
                    x = rect.left() + col * cell_size + cell_size / 2
                    y = rect.top() + row * cell_size + cell_size / 2
                    # Set stone color: black for player 1, white for player 2
                    color = Qt.GlobalColor.black if self.game_logic.board[row][col] == 1 else Qt.GlobalColor.white
                    painter.setBrush(QBrush(color))
                    painter.setPen(QPen(Qt.GlobalColor.black))
                    # Draw the stone as an ellipse
                    painter.drawEllipse(int(x - cell_size / 3), int(y - cell_size / 3),
                                        int(cell_size * 2 / 3), int(cell_size * 2 / 3))

    def mousePressEvent(self, event):
        '''Handle mouse clicks to place stones on the board.'''
        rect = self.contentsRect()  # Get the drawable area
        cell_size = min(rect.width(), rect.height()) / 7  # Ensure square cells
        col = int((event.pos().x() - rect.left()) / cell_size)
        row = int((event.pos().y() - rect.top()) / cell_size)

        # Ensure the click is within bounds
        if 0 <= row < 7 and 0 <= col < 7:
            if self.game_logic.place_stone(row, col):  # Update game logic
                self.update()  # Trigger a repaint

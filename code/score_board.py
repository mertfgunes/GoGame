from PyQt6.QtGui import QFont, QPicture, QPixmap, QFontDatabase
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtCore import pyqtSlot, Qt, QSize, QTimer
import os

from pages.gameover_page import GameOverPage


class ScoreBoard(QDockWidget):
    '''base the score_board on a QDockWidget'''

    def __init__(self):
        super().__init__()
        self.GAME_TIME = 60  # a min per each turn
        self.turnIndicator = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.counter = self.GAME_TIME
        self.timer_label = self.Text("10:00", size=32, bold=True, color="green", disableCustomFont=True)
        self.currentPlayer = self.Text("Player 1", size=28, bold=True)
        self.blackPrisioner = self.Text("0", size=24)
        self.whitePrisioner = self.Text("0", size=24)

        # Add blink timer
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink_timer_label)
        self.blink_state = True

        self.initUI()
        self.startTimer()
        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

    def initUI(self):
        self.setFixedWidth(300)
        self.setWindowTitle('ScoreBoard')
        self.setStyleSheet("""
            QDockWidget {
                background-color: #E5E7EB;
                border: none;
                color: #1F2937;
            }
            QDockWidget::title {
                font-family: 'YsabeauSC-SemiBold';
                font-size: 19px;
                font-weight: bold;
            }
            QWidget {
                background-color: #d4d4d4;
            }
            QLabel {
                color: #1F2937;
                background-color: transparent;
            }
        """)

        # Create main widget and layout
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(20, 20, 20, 20)

        # Add Prisoners section
        self.addPrisonersSection()
        self.mainLayout.addStretch()

        # Add Turn section
        self.addTurnSection()
        self.mainLayout.addStretch()

        # Set the main widget
        self.mainWidget.setLayout(self.mainLayout)
        self.setWidget(self.mainWidget)

        # Add buttons container
        buttonsWidget = QWidget()
        buttonsLayout = QHBoxLayout()

        # Add undo button
        self.undoButton = self.customButton("⎌undo", "grey")
        self.undoButton.clicked.connect(self.undoMove)
        buttonsLayout.addWidget(self.undoButton)

        # Add clear button
        self.clearButton = self.customButton("Reset", "Red")
        self.clearButton.clicked.connect(self.clearBoard)
        buttonsLayout.addWidget(self.clearButton)

        buttonsWidget.setLayout(buttonsLayout)
        self.mainLayout.addWidget(buttonsWidget)

    def skipTurn(self):
        try:
            if self.parent() and hasattr(self.parent(), 'game_logic'):
                self.parent().game_logic.skip_turn()
                self.onPlayerChange(self.parent().game_logic.current_player)  # Update the UI for the new turn
        except Exception as e:
            print(f"Error skipping turn: {e}")

    def update_timer_label(self):
        minutes, seconds = divmod(self.counter, 60)
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

        # Start blinking if 5 or fewer seconds remain
        if self.counter <= 5:
            if not self.blink_timer.isActive():
                self.blink_timer.start(500)  # Blink every 500ms
            self.timer_label.setStyleSheet("color: red;")
        else:
            if self.blink_timer.isActive():
                self.blink_timer.stop()
            self.timer_label.setStyleSheet("color: green;")
            self.blink_state = True

    def blink_timer_label(self):
        if self.blink_state:
            self.timer_label.setStyleSheet("color: transparent;")
        else:
            self.timer_label.setStyleSheet("color: red;")
        self.blink_state = not self.blink_state

    def startTimer(self):
        self.counter = self.GAME_TIME  # Reset counter
        self.update_timer_label()
        self.timer.start(1000)  # Trigger every 1 second
        if self.blink_timer.isActive():
            self.blink_timer.stop()
        self.timer_label.setStyleSheet("color: green;")
        self.blink_state = True

    def update_timer(self):
        self.counter -= 1
        self.update_timer_label()
        if self.counter <= 0:
            self.timer.stop()
            self.blink_timer.stop()
            self.timer_label.setText("Time's up!")
            self.timer_label.setStyleSheet("color: red;")

            prisoners_black = int(self.blackPrisioner.text())
            prisoners_white = int(self.whitePrisioner.text())

            # Pass the prisoner counts to the GameOverPage
            popup = GameOverPage(prisoners_black, prisoners_white)
            popup.exec()
            self.clearBoard()

    def clearBoard(self):
        """Clears all stones from the game board and resets the game state"""
        try:
            if self.parent() and hasattr(self.parent(), 'game_logic'):
                # Reset the game board
                self.parent().game_logic.board = [[0 for _ in range(self.parent().game_logic.board_size)]
                                                  for _ in range(self.parent().game_logic.board_size)]
                # Reset prisoners count
                self.parent().game_logic.prisoners_black = 0
                self.parent().game_logic.prisoners_white = 0
                # Reset current player to black (player 1)
                self.parent().game_logic.current_player = 1
                # Clear the move history
                self.parent().game_logic.board_history = []
                self.parent().game_logic.current_player_history = []

                # Update the UI
                self.parent().board.update()
                self.onPlayerChange(1)  # Reset turn indicator to player 1
                self.onPrisionerCountChange(0, 0)  # Reset prisoner counts
                self.startTimer()
        except Exception as e:
            print(f"Error in clear board: {e}")

    def undoMove(self):
        try:
            if self.parent() and hasattr(self.parent(), 'game_logic'):
                success = self.parent().game_logic.undoLastMove()
                if success:
                    self.parent().board.update()
                    self.onPlayerChange(self.parent().game_logic.current_player)
                    self.onPrisionerCountChange(self.parent().game_logic.prisoners_black,
                                                self.parent().game_logic.prisoners_white)  # Update prisoner counts
        except Exception as e:
            print(f"Error in undo: {e}")

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        # board.updateTimerSignal.connect(self.setTimeRemaining)
        board.updateTurnSignal.connect(self.onPlayerChange)
        board.updatePrisonersSignal.connect(self.onPrisionerCountChange)

    @pyqtSlot(int)
    def onPlayerChange(self, playerId):
        self.currentPlayer.setText(f"Player {playerId}")
        if playerId == 1:
            self.turnIndicator.setStyleSheet("""
                background-color: black;
                border-radius: 30px;
                border: 1.5px solid black;
            """)
        else:
            self.turnIndicator.setStyleSheet("""
                background-color: white;
                border-radius: 30px;
                border: 1.5px solid black;
            """)

        # Restart the timer for the new turn
        self.startTimer()

    @pyqtSlot(int, int)
    def onPrisionerCountChange(self, prisoners_black, prisoners_white):
        print("black: ", prisoners_black, " white: ", prisoners_white)
        self.blackPrisioner.setText(str(prisoners_black))
        self.whitePrisioner.setText(str(prisoners_white))

    @pyqtSlot(str)
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.currentPlayer.setText(clickLoc)
        print("clicked")

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemaining):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining: " + str(timeRemaining)
        self.label_timeRemaining.setText(update)
        print('slot ' + str(timeRemaining))

    def changePlayer(self):
        print(self.currentPlayer.text())
        self.currentPlayer.setText("Player 2")
        print(self.currentPlayer.text())

    def addPrisonersSection(self):
        prisonerWidget = QWidget()
        prisonerLayout = QVBoxLayout()

        # Prisoners title
        prisonerLabel = self.Text("Prisioner", size=30, bold=True)
        prisonerLayout.addWidget(prisonerLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        # Prisoner counts container
        countsWidget = QWidget()
        countsLayout = QHBoxLayout()

        # Black prisoners
        blackCountWidget = self.createPrisonerCount(self.whitePrisioner, "assets/images/whitecuff.png")

        # White prisoners
        whiteCountWidget = self.createPrisonerCount(self.blackPrisioner, "assets/images/blackcuff.png")

        countsLayout.addWidget(blackCountWidget)
        countsLayout.addWidget(whiteCountWidget)

        countsWidget.setLayout(countsLayout)
        prisonerLayout.addWidget(countsWidget)
        prisonerWidget.setLayout(prisonerLayout)

        self.mainLayout.addWidget(prisonerWidget)

    def addTurnSection(self):
        turnWidget = QWidget()
        turnWidget.setStyleSheet("background: #bfa395; border-radius: 10px;")
        turnLayout = QVBoxLayout()

        turnLabel = self.Text("Current Player", color="#92400E", size=24, bold=True)
        turnLayout.addWidget(turnLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        turnLayout.addWidget(self.Text("make you're move in"), alignment=Qt.AlignmentFlag.AlignCenter)
        turnLayout.addWidget(self.timer_label, alignment=Qt.AlignmentFlag.AlignCenter)

        currentPlayerWidget = QWidget()
        currentPlayerLayout = QHBoxLayout()

        self.turnIndicator = QLabel()
        self.turnIndicator.setFixedSize(60, 60)
        self.turnIndicator.setStyleSheet("""
            background-color: black;
            border-radius: 30px;
            border: 1.5px solid black;
        """)
        currentPlayerLayout.addWidget(self.currentPlayer, alignment=Qt.AlignmentFlag.AlignCenter)
        currentPlayerLayout.addWidget(self.turnIndicator)

        currentPlayerWidget.setLayout(currentPlayerLayout)
        turnLayout.addWidget(currentPlayerWidget, alignment=Qt.AlignmentFlag.AlignCenter)
        skipTurnBtn = self.customButton("pass", textColor="#D2B48C", color="#A67B5B")
        skipTurnBtn.clicked.connect(self.skipTurn)
        skipTurnBtn.setMinimumWidth(200)
        turnLayout.addWidget(skipTurnBtn, alignment=Qt.AlignmentFlag.AlignCenter)

        turnWidget.setLayout(turnLayout)
        self.mainLayout.addWidget(turnWidget)

    def createPrisonerCount(self, text, iconPath: str) -> QWidget:
        # Create a parent widget
        widget = QWidget()
        layout = QVBoxLayout()

        # Create the icon QLabel and set fixed size
        icon = QLabel()

        # Load and scale the image
        pixmap = QPixmap(iconPath).scaled(40, 40, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                          transformMode=Qt.TransformationMode.SmoothTransformation)
        icon.setPixmap(pixmap)

        # Apply the outer color (orange) and inner image with rounded corners
        icon.setStyleSheet("""
            QLabel {
                border-radius: 5; /* Half the size for a circular effect */
                padding: 5px; /* Padding for the image inside */
                background-color: white; /* Background color for the icon area */
            }
        """)

        layout.addWidget(icon, alignment=Qt.AlignmentFlag.AlignCenter)
        # add the text QLabel
        layout.addWidget(text, alignment=Qt.AlignmentFlag.AlignCenter)

        # Set layout to the widget
        widget.setLayout(layout)
        return widget

    def Text(self, text, color="black", size=14, bold: bool = False, disableCustomFont: bool = False):
        text = QLabel(str(text))
        if color != "black":
            text.setStyleSheet(f"color: {color};")

        # Disable custom font
        if disableCustomFont:
            font = QFont("Arial", size)
            font.setBold(bold)
            text.setFont(font)

        # set font size
        font = QFont()
        font.setPointSize(size)
        text.setFont(font)
        return text

    def customButton(self, text, color, textColor:str="white"):
        btn = QPushButton(text)
        btn.setStyleSheet(f"""
                   QPushButton {{
                       background-color: {color};                     /* Base color */
                       color: {textColor};                                 /* White text */
                       padding: 10px;                                /* Padding */
                       border-radius: 8px;                           /* Rounded corners */
                       font-size: 20px;                              /* Font size */
                   }}
                   QPushButton:hover {{
                       font-size: 24px;                              /* Font size */
                   }}
               """)
        # Set font
        return btn
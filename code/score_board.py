from PyQt6.QtGui import QFont, QPicture, QPixmap, QFontDatabase
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtCore import pyqtSlot, Qt, QSize, QTimer
import os

from pages.gameover_page import GameOverPage


class ScoreBoard(QDockWidget):
    '''base the score_board on a QDockWidget'''

    def __init__(self):
        super().__init__()
        self.GAME_TIME = 60 #1 minute per turn
        self.turnIndicator = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.counter = self.GAME_TIME
        self.timer_label = self.Text("01:00", size=32, bold=True, color="green", disableCustomFont=True)
        self.currentPlayer = self.Text("Player 1", size=32, bold=True)
        self.blackPrisioner = self.Text("0", size=24)
        self.whitePrisioner = self.Text("0", size=24)
        self.initUI()
        self.startTimer()
        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

    def startTurnTimer(self):
        self.counter = self.TURN_TIME  # resetting the counter to a min
        self.update_label()
        self.timer.start(1000)  # trigger each sec

    def update_timer(self):
        self.counter -= 1
        self.update_label()
        if self.counter <= 0:
            self.timer.stop()
            self.timer_label.setText("Time's up!")
            self.handleTimeUp()

    def handleTimeUp(self):
        # switch turn for the timer.
        self.parent().game_logic.swap_turn()
        self.onPlayerChange(self.parent().game_logic.current_player)
        self.startTurnTimer()

    @pyqtSlot(int)
    def onPlayerChange(self, playerId):
        self.currentPlayer.setText(f"Player {playerId}")
        self.startTurnTimer()  # reset the timer for each turn.

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

        self.mainLayout.addWidget(self.timer_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addStretch()

        # Set the main widget
        self.mainWidget.setLayout(self.mainLayout)
        self.setWidget(self.mainWidget)

        # Add buttons container
        buttonsWidget = QWidget()
        buttonsLayout = QHBoxLayout()

        # Add undo button
        self.undoButton = self.customButton("undo", "grey")
        self.undoButton.clicked.connect(self.undoMove)
        buttonsLayout.addWidget(self.undoButton)

        # Add clear button
        self.clearButton = self.customButton("clear", "Red")
        self.clearButton.clicked.connect(self.clearBoard)
        buttonsLayout.addWidget(self.clearButton)

        buttonsWidget.setLayout(buttonsLayout)
        self.mainLayout.addWidget(buttonsWidget)

    def update_label(self):
        minutes, seconds = divmod(self.counter, 60)
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

    def startTimer(self):
        self.counter = self.GAME_TIME  # Reset counter
        self.update_label()
        self.timer.start(1000)  # Trigger every 1 second

    def update_timer(self):
        self.counter -= 1
        self.update_label()
        if self.counter <= 0:
            self.timer.stop()
            self.timer_label.setText("Time's up!")

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
                    # Update turn indicator
                    self.onPlayerChange(self.parent().game_logic.current_player)
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
        self.currentPlayer.setText(("Player " + str(playerId)))
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

        turnLabel = self.Text("Current Player", color="#92400E", size=24)
        turnLayout.addWidget(turnLabel, alignment=Qt.AlignmentFlag.AlignCenter)

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

        # Set font
        if not disableCustomFont:
            font = QFont(self.customFont(), size)
            font.setBold(bold)
        else:
            font = QFont("Arial", size)
            font.setBold(bold)
        text.setFont(font)
        return text

    def customFont(self):
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

    def customButton(self, text, color):
        btn = QPushButton(text)
        btn.setStyleSheet(f"""
                   QPushButton {{
                       background-color: {color};                     /* Base color */
                       color: white;                                 /* White text */
                       padding: 10px;                                /* Padding */
                       border-radius: 8px;                           /* Rounded corners */
                   }}
                   QPushButton:hover {{
                       font-size: 24px;                              /* Font size */
                   }}
               """)
        # Set font
        font = QFont(self.customFont(), 20)
        btn.setFont(font)
        return btn

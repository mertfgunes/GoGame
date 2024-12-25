from PyQt6.QtGui import QFont, QPicture, QPixmap, QFontDatabase
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton
from PyQt6.QtCore import pyqtSlot, Qt, QSize
import os
from PyQt6.uic.properties import QtCore

class ScoreBoard(QDockWidget):
    '''base the score_board on a QDockWidget'''

    def __init__(self):
        super().__init__()
        self.currentPlayerText = QLabel()
        self.turnIndicator = None
        self.initUI()
        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.setFixedWidth(300)
        self.setStyleSheet("""
            QDockWidget {
                border: none;
                color: black;
            }
            QWidget {
                background-color: #d4d4d4;
            }
            QLabel {
                color: #1F2937;
                background-color: transparent;
            }
        """)
        self.setWindowTitle('ScoreBoard')

        # Create main widget and layout
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(20, 20, 20, 20)



        # Add Prisoners section
        self.addPrisonersSection()

        # Add Turn section
        self.addTurnSection()

        self.mainLayout.addStretch()
        self.mainLayout.addWidget(self.customButton("reset", "grey"))
        self.mainLayout.addWidget(self.customButton("start", "brown"))


        # Set the main widget
        self.mainWidget.setLayout(self.mainLayout)
        self.setWidget(self.mainWidget)

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)

    @pyqtSlot(str)
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location: " + clickLoc)
        print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemaining):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining: " + str(timeRemaining)
        self.label_timeRemaining.setText(update)
        print('slot ' + str(timeRemaining))

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
        self.blackCount = self.Text("2", size=24)
        blackCountWidget = self.createPrisonerCount(self.blackCount, "assets/images/whitecuff.png")

        # White prisoners
        self.whiteCount = self.Text("2", size=24)
        whiteCountWidget = self.createPrisonerCount(self.whiteCount, "assets/images/blackcuff.png")

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

        self.currentPlayerText = self.Text("Player 1", size=32, bold=True)

        self.turnIndicator = QLabel()
        self.turnIndicator.setFixedSize(60, 60)
        self.turnIndicator.setStyleSheet("""
            background-color: white;
            border-radius: 30px;
            border: 1.5px solid black;
        """)

        currentPlayerLayout.addWidget(self.currentPlayerText,  alignment=Qt.AlignmentFlag.AlignCenter)
        currentPlayerLayout.addWidget(self.turnIndicator)

        currentPlayerWidget.setLayout(currentPlayerLayout)
        turnLayout.addWidget(currentPlayerWidget, alignment=Qt.AlignmentFlag.AlignCenter)
        turnWidget.setLayout(turnLayout)

        self.mainLayout.addWidget(turnWidget)

    def changeCurrentPlayerText(self, playerId):
        if playerId == 1:
            self.currentPlayerText.setText("heli")

    def createPrisonerCount(self, text, iconPath: str) -> QWidget:
        # Create a parent widget
        widget = QWidget()
        layout = QVBoxLayout()

        # Create the icon QLabel and set fixed size
        icon = QLabel()

        # Load and scale the image
        pixmap = QPixmap(iconPath).scaled(40, 40)
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

    def Text(self, text, color="black", size=14, bold: bool = False):
        text = QLabel(str(text))
        if color != "black":
            text.setStyleSheet(f"color: {color};")

        # Set font
        font = QFont(self.customFont(), size)
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
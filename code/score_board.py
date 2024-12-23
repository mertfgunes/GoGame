from PyQt6.QtGui import QFont, QPicture, QPixmap
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt6.QtCore import pyqtSlot, Qt


class ScoreBoard(QDockWidget):
    '''base the score_board on a QDockWidget'''

    def __init__(self):
        super().__init__()
        self.initUI()

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

        # Keep original labels from template
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time remaining: ")

        # Add Prisoners section
        self.addPrisonersSection()

        # Add Turn section
        self.addTurnSection()

        # Add original labels from template
        self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayout.addWidget(self.label_timeRemaining)

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
        prisonerLabel = self.Text("Prisioner", size=24, bold=True)
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

        self.currentPlayerText = self.Text("Getty", size=32, bold=True)

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

    def Text(self, text, color="black", size=12, bold: bool = False):
        text = QLabel(str(text))
        if color != "black":
            text.setStyleSheet(f"color: '{color}';")
        font = QFont("Arial", size)
        font.setBold(bold)
        text.setFont(font)
        return text

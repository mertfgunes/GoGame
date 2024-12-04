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
                background-color: #E5E7EB;
                border: none;
            }
            QWidget {
                background-color: #E5E7EB;
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
        self.mainLayout.setSpacing(30)
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
        prisonerLayout.setSpacing(15)
        
        # Prisoners title
        prisonerLabel = QLabel("Prisoners")
        prisonerLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        prisonerLayout.addWidget(prisonerLabel)
        
        # Prisoner counts container
        countsWidget = QWidget()
        countsLayout = QHBoxLayout()
        countsLayout.setSpacing(20)
        
        # Black prisoners
        self.blackCount = QLabel("9")
        blackCountWidget = self.createPrisonerCount("black", self.blackCount)
        
        # White prisoners
        self.whiteCount = QLabel("1")
        whiteCountWidget = self.createPrisonerCount("white", self.whiteCount)
        
        countsLayout.addWidget(blackCountWidget)
        countsLayout.addWidget(whiteCountWidget)
        countsLayout.addStretch()
        
        countsWidget.setLayout(countsLayout)
        prisonerLayout.addWidget(countsWidget)
        prisonerWidget.setLayout(prisonerLayout)
        
        self.mainLayout.addWidget(prisonerWidget)

    def addTurnSection(self):
        turnWidget = QWidget()
        turnLayout = QVBoxLayout()
        turnLayout.setSpacing(15)
        
        turnLabel = QLabel("TURN")
        turnLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        turnLayout.addWidget(turnLabel)
        
        playerWidget = QWidget()
        playerLayout = QHBoxLayout()
        
        self.playerLabel = QLabel("Getty")
        self.playerLabel.setStyleSheet("font-size: 32px; font-weight: bold;")
        
        self.turnIndicator = QLabel()
        self.turnIndicator.setFixedSize(40, 40)
        self.turnIndicator.setStyleSheet("""
            background-color: black;
            border-radius: 20px;
        """)
        
        playerLayout.addWidget(self.playerLabel)
        playerLayout.addWidget(self.turnIndicator)
        playerLayout.addStretch()
        
        playerWidget.setLayout(playerLayout)
        turnLayout.addWidget(playerWidget)
        turnWidget.setLayout(turnLayout)
        
        self.mainLayout.addWidget(turnWidget)

    def createPrisonerCount(self, color, countLabel):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        stone = QLabel()
        stone.setFixedSize(32, 32)
        if color == "black":
            stone.setStyleSheet("background-color: black; border-radius: 16px;")
        else:
            stone.setStyleSheet("""
                background-color: white;
                border: 1px solid black;
                border-radius: 16px;
            """)
        
        countLabel.setStyleSheet("font-size: 20px; font-weight: bold;")
        
        layout.addWidget(stone)
        layout.addWidget(countLabel)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
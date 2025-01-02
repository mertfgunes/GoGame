from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from .tutorial_page import TutorialPage

class WelcomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title = QLabel("Welcome to Go")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 48px;
            }
        """)
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        buttons = [
            ("Play Game", "#92400E", self.startGame),
            ("Tutorial", "#4B5563", self.showTutorial),
            ("Exit", "#DC2626", self.close)
        ]
        
        for text, color, callback in buttons:
            btn = QPushButton(text)
            btn.setFixedSize(200, 50)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 18px;
                }}
                QPushButton:hover {{
                    background-color: {color}DD;
                    font-size: 20px;
                }}
            """)
            btn.clicked.connect(callback)
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("background-color: #1a1a1a;")

    def startGame(self):
        if self.parent():
            self.parent().startGame()

    def showTutorial(self):
        tutorial = TutorialPage(self.parent())
        if self.parent():
            self.parent().switchToTutorial(tutorial)
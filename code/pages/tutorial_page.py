# tutorial_page.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                           QScrollArea, QFrame)
from PyQt6.QtCore import Qt

class TutorialPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    def goBack(self):
        if self.parent():
            self.parent().showWelcome()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #1a1a1a;
            }
            QScrollBar:vertical {
                background: #2d2d2d;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #4a4a4a;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #5a5a5a;
            }
        """)

        # Content widget
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("How to Play Go")
        title.setStyleSheet("""
            color: white;
            font-size: 36px;
            font-family: 'YsabeauSC-SemiBold', sans-serif;
            margin-bottom: 20px;
        """)
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Rules content (keep your existing rules content)
        rules = [
            ("Basic Rules", [
                "• Players take turns placing stones on intersections",
                "• Black plays first",
                "• Stones cannot be moved once placed",
                "• Adjacent stones of the same color form groups"
            ]),
            ("Capturing Stones", [
                "• Surround opponent's stones to capture them",
                "• Stones need empty adjacent points (liberties) to survive",
                "• Captured stones are removed from the board",
                "• Captured stones count as prisoners"
            ]),
            ("Winning the Game", [
                "• Control more territory than your opponent",
                "• Territory is empty points surrounded by your stones",
                "• Each captured stone counts as one point",
                "• Game ends when both players pass consecutively"
            ])
        ]
        
        for section_title, section_rules in rules:
            section_label = QLabel(section_title)
            section_label.setStyleSheet("""
                color: #92400E;
                font-size: 24px;
                font-weight: bold;
                margin-top: 20px;
            """)
            layout.addWidget(section_label)
            
            for rule in section_rules:
                rule_label = QLabel(rule)
                rule_label.setStyleSheet("""
                    color: white;
                    font-size: 18px;
                    margin: 5px 0;
                """)
                layout.addWidget(rule_label)
        
        # Back button
        backBtn = QPushButton("Back to Menu")
        backBtn.setFixedSize(200, 50)
        backBtn.setStyleSheet("""
            QPushButton {
                background-color: #4B5563;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #374151;
                font-size: 20px;
            }
        """)
        backBtn.clicked.connect(self.goBack)
        layout.addWidget(backBtn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Set the content widget in scroll area
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        self.setStyleSheet("background-color: #1a1a1a;")
        self.setMinimumSize(600, 400)  # Set minimum window size
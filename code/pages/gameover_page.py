from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QDialog, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFontDatabase, QFont
import os


class GameOverPage(QDialog):
    def __init__(self, blackPrisoner: int, whitePrisoner: int, parent=None):
        super().__init__(parent)
        self.blackPrisoner = blackPrisoner
        self.whitePrisoner = whitePrisoner

        # Set window title and minimum size
        self.setWindowTitle("Game Over")
        self.setMinimumSize(600, 600)
        self.setGeometry(305, 210, 600, 600)
        self.setStyleSheet("background-color: #9e9e9e;")

        # Main layout
        layout = QVBoxLayout()

        # Winner image
        winner_label = QLabel()
        winner_img_path = os.path.abspath("../assets/images/winner.png")
        winner_pixmap = QPixmap(winner_img_path)
        winner_label.setPixmap(winner_pixmap)

        # Title and Winner Details
        self.title = self.Text("Winner", size=64, bold=True, color="#C04000")
        self.subTitle = self.Text("0-0", size=36, color="#36454F")
        self.winnerText = self.Text("", size=42, color="#800020")
        self.winnerColor = self.Text("", size=82, bold=True)
        self.winner()

        layout.addWidget(winner_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.winnerText, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.winnerColor, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.subTitle, alignment=Qt.AlignmentFlag.AlignCenter)

        btnLayout = QHBoxLayout()

        # New Game button
        new_game_btn = QPushButton("New Game")
        new_game_btn.setStyleSheet("""
            QPushButton {
                background-color: #00A36C;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-size: 16px;
                font-family: 'YsabeauSC-SemiBold';
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: green;
            }
        """)

        # Exit Game button
        exit_btn = QPushButton("Quit Game")
        exit_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #A9A9A9;
                        color: white;
                        padding: 10px;
                        border-radius: 8px;
                        font-size: 16px;
                        font-family: 'YsabeauSC-SemiBold';
                        min-width: 100px;
                    }
                    QPushButton:hover {
                        background-color: red;
                    }
                """)

        exit_btn.clicked.connect(QApplication.instance().quit)
        new_game_btn.clicked.connect(self.close)

        btnLayout.addWidget(exit_btn)
        btnLayout.addWidget(new_game_btn)

        layout.addLayout(btnLayout)

        self.setLayout(layout)
        self.setStyleSheet("""
            QDialog {
                background-color: #E5E7EB;
            }
        """)

    def winner(self):
        if self.blackPrisoner > self.whitePrisoner:
            self.winnerText.setText("Player 2")
            self.winnerColor.setText("White")
            self.winnerColor.setStyleSheet("""color: white; font-size: 62px""")  # Corrected method
            self.subTitle.setText(f"{self.blackPrisoner} - {self.whitePrisoner}")
        elif self.blackPrisoner < self.whitePrisoner:
            self.winnerText.setText("Player 1")
            self.winnerColor.setText("Black")
            self.winnerColor.setStyleSheet("""color: black; font-size: 62px""")  # Corrected method
            self.subTitle.setText(f"{self.whitePrisoner} - {self.blackPrisoner}")
        else:
            self.title.setText("Draw Match")
            self.winnerText.hide()
            self.winnerColor.hide()
            self.subTitle.setText(f"{self.blackPrisoner} - {self.whitePrisoner}")

    def Text(self, text, color="black", size=14, bold: bool = False):
        label = QLabel(str(text))
        if color != "black":
            label.setStyleSheet(f"color: {color};")
            font = QFont()
            font.setPointSize(size)
            font.setBold(bold)
            label.setFont(font)

        return label

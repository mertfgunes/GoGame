from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import QTimer

class TimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Timer Example")
        self.layout = QVBoxLayout()

        # Label to display timer
        self.timer_label = QLabel("02:00", self)
        self.timer_label.setStyleSheet("font-size: 30px;")
        self.layout.addWidget(self.timer_label)

        # Button to start timer
        self.start_button = QPushButton("Start Timer", self)
        self.start_button.clicked.connect(self.start_timer)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

        # Timer setup
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.counter = 120

    def start_timer(self):
        self.counter = 120  # Reset counter (you can adjust for a custom time)
        self.update_label()  # Ensure the initial value is displayed
        self.timer.start(1000)  # Trigger every 1 second

    def update_timer(self):
        self.counter -= 1
        self.update_label()
        if self.counter <= 0:
            self.timer.stop()
            self.timer_label.setText("Time's up!")

    def update_label(self):
        minutes, seconds = divmod(self.counter, 60)
        self.timer_label.setText(f"{minutes:02}:{seconds:02}")

if __name__ == "__main__":
    app = QApplication([])
    window = TimerApp()
    window.show()
    app.exec()

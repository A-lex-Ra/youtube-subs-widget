from googleapiclient.discovery import build
from keys import api_key

youtube = build("youtube", "v3", developerKey=api_key)

class SubsCount:
    @staticmethod
    def _get_subs_count(**kwargs) -> int | None:
        try:
            request = youtube.channels().list(part="statistics", **kwargs)
            response = request.execute()
            items = response.get("items", [])
            if not items:
                print(f"[Error] Channel not found for parameters: {kwargs}")
                return None
            return int(items[0]["statistics"]["subscriberCount"])
        except Exception as e:
            print(f"[Error] API call failed: {e}")
            return None

    @classmethod
    def by_id(cls, channel_id: str) -> int | None:
        return cls._get_subs_count(id=channel_id)

    @classmethod
    def by_handle(cls, channel_handle: str) -> int | None:
        return cls._get_subs_count(forHandle=channel_handle)

##
##channel_handle = "@MrBeast"
##print(f"Searching for channel {channel_handle}...")
##print(SubsCount.by_handle(channel_handle),
##      "is current subs count.")
##print()
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import QTimer
from datetime import datetime

class SubsCheckerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Subs Checker")
        self.setGeometry(100, 100, 350, 150)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter channel handle (e.g., @MyChannel)")
        self.layout.addWidget(self.input)

        self.button = QPushButton("Check Now")
        self.button.clicked.connect(self.update_subs)
        self.layout.addWidget(self.button)

        self.label = QLabel("Subscribers: -")
        self.label.setStyleSheet("font-size: 18px;")
        self.layout.addWidget(self.label)

        self.last_updated = None  # UPD time

        self.updated_label = QLabel("Last updated: never")
        self.updated_label.setStyleSheet("font-size: 12px; color: gray;")
        self.layout.addWidget(self.updated_label)

        # Timer "X min ago"
        self.elapsed_timer = QTimer(self)
        self.elapsed_timer.timeout.connect(self.update_elapsed_time)
        self.elapsed_timer.start(60 * 1000)  # 1 min

        # ⏲️ 10 min timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_subs)
        self.timer.start(10 * 60 * 1000)  # 10 минут

    def update_subs(self):
        handle = self.input.text().strip()
        if not handle.startswith("@"):
            QMessageBox.warning(self, "Invalid Handle", "Channel handle must start with '@'.")
            return

        self.label.setText("Checking...")
        count = SubsCount.by_handle(handle)
        if count is not None:
            self.last_updated = datetime.now()
            self.label.setText(f"Subscribers: {count:,}")
            self.update_elapsed_time()
        else:
            self.label.setText("Subscribers: ? (error)")

    def update_elapsed_time(self):
        if self.last_updated is None:
            self.updated_label.setText("Last updated: never")
            return

        delta = datetime.now() - self.last_updated
        minutes = delta.total_seconds() // 60
        if minutes < 1:
            self.updated_label.setText("Last updated: just now")
        elif minutes == 1:
            self.updated_label.setText("Last updated: 1 minute ago")
        else:
            self.updated_label.setText(f"Last updated: {int(minutes)} minutes ago")



# 🚀 Launch
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SubsCheckerApp()
    window.show()
    sys.exit(app.exec_())

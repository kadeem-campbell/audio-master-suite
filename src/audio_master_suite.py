import sys
import os
import threading
import subprocess
import shutil

from PyQt6.QtCore import pyqtSignal, QObject, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QProgressBar,
    QTextEdit,
    QMainWindow,
    QFileDialog,
)

class WorkerSignals(QObject):
    progress = pyqtSignal(int)
    log = pyqtSignal(str)
    finished = pyqtSignal()

class AudioMasterSuite(QMainWindow):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()
        self.signals.progress.connect(self.update_progress)
        self.signals.log.connect(self.append_log)
        self.signals.finished.connect(self.process_finished)

        self.queue_dir = os.path.join(os.path.expanduser("~"), "Desktop", "Mastering_Queue")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Audio Master Suite")
        self.setFixedSize(600, 500)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.setStyleSheet(
            "QMainWindow { background-color: #121212; }"
            "QLabel { color: #e0e0e0; font-size: 20px; font-weight: bold; }"
            "QPushButton { background-color: #1db954; color: white; border-radius: 5px; padding: 10px; font-weight: bold; }"
            "QTextEdit { background-color: #181818; color: #b3b3b3; font-family: 'Courier New'; }"
        )

        layout.addWidget(QLabel("CD WAV CONVERTER", alignment=Qt.AlignmentFlag.AlignCenter))

        self.select_btn = QPushButton("SELECT AUDIO FILES")
        self.select_btn.clicked.connect(self.pick_files)
        layout.addWidget(self.select_btn)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        layout.addWidget(self.log_box)

        self.append_log("Ready. Converts files to 44.1kHz, 16-bit, stereo WAV in ~/Desktop/Mastering_Queue")

    def pick_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Audio",
            "",
            "Audio Files (*.mp3 *.wav *.m4a *.flac *.aiff *.aac *.ogg)",
        )
        if not files:
            return

        self.select_btn.setEnabled(False)
        threading.Thread(target=self.convert_files, args=(files,), daemon=True).start()

    def convert_files(self, files):
        if shutil.which("ffmpeg") is None:
            self.signals.log.emit("ffmpeg not found. Install it first (brew install ffmpeg).")
            self.signals.progress.emit(0)
            self.signals.finished.emit()
            return

        if os.path.exists(self.queue_dir):
            shutil.rmtree(self.queue_dir)
        os.makedirs(self.queue_dir, exist_ok=True)

        total = len(files)
        for i, f in enumerate(files, start=1):
            out_name = f"Track_{i:02d}.wav"
            out_path = os.path.join(self.queue_dir, out_name)

            self.signals.log.emit(f"Converting: {os.path.basename(f)} -> {out_name}")

            subprocess.run(
                ["ffmpeg", "-y", "-i", f, "-ar", "44100", "-ac", "2", "-sample_fmt", "s16", out_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )

            self.signals.progress.emit(int(i / total * 100))

        self.signals.finished.emit()

    def append_log(self, msg):
        self.log_box.append(msg)

    def update_progress(self, val):
        self.progress_bar.setValue(val)

    def process_finished(self):
        self.append_log("Done.")
        self.select_btn.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    window = AudioMasterSuite()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

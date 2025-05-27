import wave
import contextlib
import math
import time
import speech_recognition as sr
from moviepy import AudioFileClip
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal


class Ui_MainWindow(object):
    def __init__(self):
        self.mp4_file_name = ""
        self.output_file = ""
        self.audio_file = "speech.wav"

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        # SELECTED VIDEO FILE
        self.label = QtWidgets.QLabel("Selected File Directory:")
        self.label.setFont(QtGui.QFont("Hammersmith One", 11))  # Custom font
        self.selected_video_label = QtWidgets.QLabel("")
        self.selected_video_label.setFont(QtGui.QFont("Hammersmith One", 10))
        self.selected_video_label.setFrameShape(QtWidgets.QFrame.Box)
        self.selected_video_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        file_layout = QtWidgets.QHBoxLayout()
        file_layout.addWidget(self.label)
        file_layout.addWidget(self.selected_video_label, stretch=1)
        main_layout.addLayout(file_layout)

        # OUTPUT FILE NAME
        self.label_3 = QtWidgets.QLabel("Add File Name:")
        self.label_3.setFont(QtGui.QFont("Hammersmith One", 11))
        self.output_file_name = QtWidgets.QLineEdit()
        self.output_file_name.setFont(QtGui.QFont("Hammersmith One", 11))
        self.output_file_name.setPlaceholderText("example.txt")
        self.output_file_name.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        output_layout = QtWidgets.QHBoxLayout()
        output_layout.addWidget(self.label_3)
        output_layout.addWidget(self.output_file_name)
        main_layout.addLayout(output_layout)

        # Transcribe button
        self.transcribe_button = QtWidgets.QPushButton("Transcribe")
        self.transcribe_button.setFont(QtGui.QFont("Hammersmith One", 11))
        self.transcribe_button.setEnabled(False)
        self.transcribe_button.clicked.connect(self.process_and_transcribe_audio)

        # Progress bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setProperty("value", 0)

        # Save button
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setFont(QtGui.QFont("Hammersmith One", 11))
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_transcribed_text)

        progress_layout = QtWidgets.QHBoxLayout()
        progress_layout.addWidget(self.transcribe_button)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.save_button)
        main_layout.addLayout(progress_layout)

        # Converted Text
        self.label_5 = QtWidgets.QLabel("Converted Text:")
        self.label_5.setFont(QtGui.QFont("Hammersmith One", 11))
        self.transcribed_text = QtWidgets.QTextBrowser()

        main_layout.addWidget(self.label_5)
        main_layout.addWidget(self.transcribed_text)

        # Message label
        self.message_label = QtWidgets.QLabel("")
        self.message_label.setFont(QtGui.QFont("Hammersmith One", 11))
        self.message_label.setFrameShape(QtWidgets.QFrame.Box)
        self.message_label.setObjectName("message_label")
        main_layout.addWidget(self.message_label)

        self.centralwidget.setLayout(main_layout)
        MainWindow.setCentralWidget(self.centralwidget)

        # Menubar and Statusbar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.menuFile = QtWidgets.QMenu("File")
        self.menuAbout = QtWidgets.QMenu("About")
        self.actionOpen_mp4_video_recording = QtWidgets.QAction("Open MP4 Video Recording")
        self.actionOpen_mp4_video_recording.triggered.connect(self.open_audio_file)
        self.actionNew = QtWidgets.QAction("New")
        self.actionNew.triggered.connect(self.new_project)
        self.actionAbout_vid2text = QtWidgets.QAction("About VID2TEXT")
        self.actionAbout_vid2text.triggered.connect(self.show_about)

        self.menuFile.addAction(self.actionOpen_mp4_video_recording)
        self.menuFile.addAction(self.actionNew)
        self.menuAbout.addAction(self.actionAbout_vid2text)
        self.menubar.addMenu(self.menuFile)
        self.menubar.addMenu(self.menuAbout)

        MainWindow.setWindowTitle("VID2TEXT CONVERTER")
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def open_audio_file(self):
        file_name = QFileDialog.getOpenFileName()
        if file_name[0].lower().endswith(".mp4"):
            self.transcribe_button.setEnabled(True)
            self.mp4_file_name = file_name[0]
            self.message_label.setText("")
            self.selected_video_label.setText(file_name[0])
        else:
            self.message_label.setText("Please Select an *.mp4 file")

    def convert_mp4_to_wav(self):
        self.message_label.setText("Converting mp4 to audio (*.wav)...")
        self.convert_thread = convertVideoToAudioThread(self.mp4_file_name, self.audio_file)
        self.convert_thread.finished.connect(self.finished_converting)
        self.convert_thread.start()

    def get_audio_duration(self, audio_file):
        with contextlib.closing(wave.open(audio_file, "r")) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration

    def transcribe_audio(self, audio_file):
        total_duration = math.ceil(self.get_audio_duration(audio_file) / 10)
        self.td = total_duration
        self.output_file = self.output_file_name.text() or "my_speech_file.txt"

        self.thread = transcriptionThread(total_duration, audio_file, self.output_file)
        self.thread.finished.connect(self.finished_)
        self.thread.change_value.connect(self.set_progress_value)
        self.thread.start()

    def finished_converting(self):
        self.message_label.setText(" file...")
        self.transcribe_audio(self.audio_file)

    def finished_(self):
        self.progress_bar.setValue(100)
        self.transcribe_button.setEnabled(True)
        self.save_button.setEnabled(True)
        self.message_label.setText("")
        self.update_text_output()

    def set_progress_value(self, val):
        increment = int(math.floor(100 * (float(val) / self.td)))
        self.progress_bar.setValue(increment)

    def process_and_transcribe_audio(self):
        self.transcribe_button.setEnabled(False)
        self.message_label.setText("Converting mp4 to audio (*.wav)...")
        self.convert_mp4_to_wav()

    def update_text_output(self):
        with open(self.output_file, "r") as f:
            self.transcribed_text.setText(f.read())

    def new_project(self):
        self.message_label.setText("")
        self.transcribed_text.setText("")
        self.selected_video_label.setText("")
        self.output_file_name.setText("")
        self.progress_bar.setValue(0)
        self.save_button.setEnabled(False)

    def show_about(self):
        msg = QMessageBox()
        msg.setWindowTitle("About VID2TEXT")
        msg.setText(" Created by Pritam Satpute and Team,\n Students,\n Computer Science & Engineering,\n Guru Nanak Institute of Technology, Nagpur")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def save_transcribed_text(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            None,
            "Save Transcription As",
            self.output_file_name.text() or "my_speech_file.txt",
            "Text Files (*.txt);;All Files (*)",
            options=options
        )
        if filename:
            if not filename.lower().endswith(".txt"):
                filename += ".txt"
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.transcribed_text.toPlainText())
                self.message_label.setText(f"Saved to {filename}")
            except Exception as e:
                self.message_label.setText(f"Error Saving File: {e}")


class convertVideoToAudioThread(QThread):
    def __init__(self, mp4_file_name, audio_file):
        QThread.__init__(self)
        self.mp4_file_name = mp4_file_name
        self.audio_file = audio_file

    def __del__(self):
        self.wait()

    def run(self):
        audio_clip = AudioFileClip(self.mp4_file_name)
        audio_clip.write_audiofile(self.audio_file)


class transcriptionThread(QThread):
    change_value = pyqtSignal(int)

    def __init__(self, total_duration, audio_file, output_file):
        QThread.__init__(self)
        self.total_duration = total_duration
        self.audio_file = audio_file
        self.output_file = output_file

    def __del__(self):
        self.wait()

    def run(self):
        r = sr.Recognizer()
        for i in range(0, self.total_duration):
            try:
                with sr.AudioFile(self.audio_file) as source:
                    audio = r.record(source, offset=i * 10, duration=10)
                    with open(self.output_file, "a") as f:
                        f.write(r.recognize_google(audio))
                        f.write(" ")
                self.change_value.emit(i)
            except:
                print("Unknown Word Detected...")
                continue


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("""
    QWidget {
        background-color: #E5D9F2;
        color: #2c3e50;
    }
    QLabel {
        color: #2d3436;
    }
    QPushButton {
        background-color: #A294F9;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
    }
    QPushButton:hover {
        background-color: #CDC1FF;
    }
    QPushButton:disabled {
        background-color: #A294F9;
    }
    QLineEdit, QTextBrowser {
        border: 1px solid #CDC1FF;
        background-color: #ffffff;
        padding: 8px;
        border-radius: 6px;
        font-family: Consolas, monospace;
        font-size: 11pt;
    }
    QProgressBar {
        height: 25px;
        text-align: center;
        border-radius: 12px;
        background-color: #CDC1FF;
        font-size: 13pt;
        font-weight: bold;
    }
    QProgressBar::chunk {
        background-color: #A294F9;
        border-radius: 12px;
    }
    QMenuBar {
        background-color: #A294F9;
    }
    QMenuBar::item {
        background: transparent;
        padding: 6px 12px;
    }
    QMenuBar::item:selected {
        background-color: #CDC1FF;
    }
    QMenu {
        background-color: #CDC1FF;
        border: 1px solid #bdc3c7;
    }
    QMenu::item {
        background-color: #CDC1FF;
        padding: 6px 20px;
    }
    QMenu::item:selected {
        background-color: #3498db;
        color: white;
    }
    QLabel#message_label {
        border: 1px solid #CDC1FF;
        background-color: #ffffff;
        padding: 5px;
        color: #c0392b;
    }
    """)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

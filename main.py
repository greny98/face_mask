import sys
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot, QRect, QSize, QTimer, QRunnable, QThreadPool
from PyQt5.QtGui import QImage, QPixmap, QMovie
from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

import cv2
import time

from detection import predict, utils
from ui_loading_screen import Ui_LoadingScreen
from assistant import process
import pyttsx3

engine = pyttsx3.init()


class FaceMaskThread(QThread):
    changePixmap = pyqtSignal(QImage)
    is_running = True
    is_stopping_check_mask = False

    @pyqtSlot(bool)
    def getStatusFromApp(self, status):
        self.is_running = status

    @pyqtSlot(bool)
    def setCheckMask(self, status):
        self.is_stopping_check_mask = status

    def run(self):
        path_dict = {
            'checkpoint': 'configs/my_ckpt/ckpt-5',
            'pipeline': 'configs/custom.config',
            'label_map': 'configs/label_map.pbtxt'
        }
        model = utils.load_model(path_dict)
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if not self.is_stopping_check_mask:
                frame = predict.execute(frame, model, engine)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(
                rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_qt_format.scaled(960, 720, Qt.KeepAspectRatio)

            cv2.waitKey(3) & 0xFF
            self.changePixmap.emit(p)
            if not self.is_running:
                # self.terminate()
                break


class VoiceAssistantThread(QThread):
    def __init__(self, showVoice, hideVoice, showLoading, hideLoading):
        super(VoiceAssistantThread, self).__init__()
        self.showVoice = showVoice
        self.hideVoice = hideVoice
        self.showLoading = showLoading
        self.hideLoading = hideLoading

    def run(self):
        process.run(engine, self.showVoice, self.hideVoice, self.showLoading, self.hideLoading)


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.threadPool = QThreadPool()
        self.setupUi()
        self.executeFaceThread()

    def setupUi(self):
        self.setWindowTitle("Face Mask Detection")
        self.setWindowIcon(QtGui.QIcon("icon/face_chibi.png"))
        self.resize(1200, 860)
        self.centralwidget = QWidget(self)

        # create button start voice
        self.btn_voice = QPushButton(self.centralwidget)
        self.btn_voice.setGeometry(QRect(1050, 50, 101, 41))
        self.btn_voice.setObjectName("btn_voice")
        self.btn_voice.setText("Start Voice")
        self.btn_voice.clicked.connect(self.evt_btn_voice_clicked)
        # create icon loading
        self.labelLoading = QLabel(self)
        self.labelLoading.move(940, 0)
        self.movie = QMovie("icon/loader.gif")
        self.labelLoading.setMovie(self.movie)
        # create a label
        self.label = QLabel(self)
        self.label.setGeometry(QRect(40, 40, 960, 720))
        self.label.setMinimumSize(QSize(960, 720))
        self.label.setMaximumSize(QSize(960, 720))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.setStyleSheet("border:0.5px solid #CCC")
        self.show()

    def showLoading(self):
        print('Show loading')
        self.movie.start()

    def hideLoading(self):
        print('hide loading')
        self.movie.stop()

    def showVoiceIcon(self):
        self.btn_voice.setIcon(QtGui.QIcon("icon/micro.png"))

    def hideVoiceIcon(self):
        self.btn_voice.setIcon(QtGui.QIcon())

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def executeFaceThread(self):
        self.faceThread = FaceMaskThread()
        self.faceThread.changePixmap.connect(self.setImage)
        self.faceThread.start()

    def evt_btn_voice_clicked(self):
        self.faceThread.setCheckMask(True)
        self.voiceThread = VoiceAssistantThread(self.showVoiceIcon, self.hideVoiceIcon, self.showLoading,
                                                self.hideLoading)
        self.voiceThread.start()
        self.btn_voice.setText("Stop Voice")
        self.btn_voice.setEnabled(False)
        self.voiceThread.finished.connect(self.evt_voice_thread_finished)

    def evt_voice_thread_finished(self):
        self.faceThread.setCheckMask(False)
        self.btn_voice.setText("Start Voice")
        self.btn_voice.setEnabled(True)


    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.faceThread.getStatusFromApp(False)
        time.sleep(1)


class LoadingApp(QMainWindow):
    def __init__(self):
        super(LoadingApp, self).__init__()
        self.ui = Ui_LoadingScreen()
        self.ui.setupUi(self)

        self.counter = 0

        # REMOVE TITLE BAR
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        # QTIMER
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(30)

        self.ui.label_description.setText(
            "<strong>WELCOME</strong> TO MY APPLICATION")
        QTimer.singleShot(4500, lambda: self.ui.label_description.setText(
            "<strong>LOADING</strong> DATABASE"))
        QTimer.singleShot(10000, lambda: self.ui.label_description.setText(
            "<strong>LOADING</strong> USER INTERFACE"))
        # SHOW ==> MAIN WINDOW

    def progress(self):
        self.counter += 0.4
        self.ui.progressBar.setValue(self.counter)
        if self.counter > 100:
            self.timer.stop()
            # SHOW MAIN WINDOW
            self.main = App()
            self.main.show()
            # CLOSE Loading SCREEN
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())

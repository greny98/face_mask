import sys
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot, QRect, QSize, QTimer
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

import cv2
import time

from detection import predict, utils
from loading_progress_bar import Loading_Progressbar
from loading_circle_bar import Loading_CircleBar

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
    def stopCheckMask(self, status):
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
                break


class VoiceAssistantThread(QThread):
    def __init__(self, showVoice, hideVoice):
        super(VoiceAssistantThread, self).__init__()
        self.showVoice = showVoice
        self.hideVoice = hideVoice

    def run(self):
        process.run(engine, self.showVoice, self.hideVoice)


class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        self.setupUi()
        # activate face-thread
        self.executeFaceThread()
    # UI for Main App
    def setupUi(self):
        # Config common for App
        self.setWindowTitle("Face Mask Detector")
        self.setWindowIcon(QIcon("icon/face_chibi.png"))
        self.resize(1200, 860)
        self.setStyleSheet(u"background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #3399FF, stop:1 #66B2FF);")

        self.centralwidget = QWidget(self)
        self.btn_voice = QPushButton(self.centralwidget)
        self.btn_voice.setStyleSheet(u"QPushButton{\n"
                                      "	border-radius: 20px;\n"
                                      "	background-color: rgba(255, 255, 255, 120);\n"
                                      "}")
        self.btn_voice.setGeometry(QRect(550, 40, 100, 40))
        self.btn_voice.setObjectName("btn_voice")
        self.btn_voice.setText("Start Voice")
        self.btn_voice.clicked.connect(self.evt_btn_voice_clicked)
        # TODO:reate icon loading

        # create a label
        self.label = QLabel(self)
        self.label.setStyleSheet("QLabel{ background-color: rgba(255, 255, 255, 120) }")
        self.label.setGeometry(QRect(120, 100, 960, 720))
        self.label.setMinimumSize(QSize(960, 720))
        self.label.setMaximumSize(QSize(960, 720))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.setStyleSheet("border:0.5px solid #CCC")

    def showVoiceIcon(self):
        self.btn_voice.setIcon(QtGui.QIcon("icon/micro.png"))

    def hideVoiceIcon(self):
        self.btn_voice.setIcon(QtGui.QIcon())

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def executeFaceThread(self):
        self.faceThread = FaceMaskThread()
        self.faceThread.start()
        self.faceThread.changePixmap.connect(self.setImage)

    def evt_btn_voice_clicked(self):
        self.faceThread.stopCheckMask(True)
        self.voiceThread = VoiceAssistantThread(
            self.showVoiceIcon, self.hideVoiceIcon)
        self.voiceThread.start()
        self.btn_voice.setText("Stop Voice")
        self.btn_voice.setEnabled(False)
        self.voiceThread.finished.connect(self.evt_voice_thread_finished)

    def evt_voice_thread_finished(self):
        self.faceThread.stopCheckMask(False)
        self.btn_voice.setText("Start Voice")
        self.btn_voice.setEnabled(True)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.faceThread.getStatusFromApp(False)
        time.sleep(1)


class LoadingProgressApp(QMainWindow):
    def __init__(self):
        super(LoadingProgressApp, self).__init__()
        self.ui = Loading_Progressbar()
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
            # self.main = App()
            # self.main.show()
            # CLOSE Loading SCREEN
            self.close()


class LoadingCircleApp(QMainWindow):
    def __init__(self):
        super(LoadingCircleApp, self).__init__()
        self.ui = Loading_CircleBar()
        self.ui.setupUi(self)

        # create params
        self.counter = 0
        self.jumper = 10

        # ==> SET INITIAL PROGRESS BAR TO (0) ZERO
        self.progressBarValue(0)

        # ==> REMOVE STANDARD TITLE BAR
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove title bar
        # Set background to transparent
        self.setAttribute(Qt.WA_TranslucentBackground)

        # ==> APPLY DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.ui.circularBg.setGraphicsEffect(self.shadow)

        # QTIMER ==> START
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(20)

        # SHOW ==> MAIN WINDOW
        ########################################################################
    def progress(self):
        value = self.counter

        # HTML TEXT PERCENTAGE
        htmlText = """<p><span style=" font-size:68pt;">{VALUE}</span><span style=" font-size:58pt; vertical-align:super;">%</span></p>"""
        # REPLACE VALUE
        newHtml = htmlText.replace("{VALUE}", str(self.jumper))
        if(value > self.jumper):
            # APPLY NEW PERCENTAGE TEXT
            self.ui.labelPercentage.setText(newHtml)
            self.jumper += 10

        # SET VALUE TO PROGRESS BAR
        # fix max value error if > than 100
        if value >= 100:
            value = 1.000
        self.progressBarValue(value)

        if self.counter > 100:
            # STOP TIMER
            self.timer.stop()
            # SHOW MAIN WINDOW
            self.main = App()
            self.main.show()
            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        self.counter += 0.5

    # DEF PROGRESS BAR VALUE
    ########################################################################
    def progressBarValue(self, value):
        # PROGRESSBAR STYLESHEET BASE
        styleSheet = """
        QFrame{
        	border-radius: 200px;
        	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} rgba(85, 170, 255, 255));
        }
        """
        # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
        # stop works of 1.000 to 0.000
        progress = (100 - value) / 100.0
        # GET NEW VALUES
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)

        # SET VALUES TO NEW STYLESHEET
        newStylesheet = styleSheet.replace(
            "{STOP_1}", stop_1).replace("{STOP_2}", stop_2)
        # APPLY STYLESHEET WITH NEW VALUES
        self.ui.circularProgress.setStyleSheet(newStylesheet)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoadingCircleApp()
    window.show()
    sys.exit(app.exec())

import sys
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot, QRect, QSize
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *

import cv2
import time

from detection import predict, utils
from ui_loading_screen import Ui_LoadingScreen

counter = 0


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    is_running = True

    @pyqtSlot(bool)
    def getStatusFromApp(self, status):
        self.is_running = status

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
            frame = predict.execute(frame, model)
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


class App(QWidget):
    def __init__(self, thread):
        super().__init__()
        self.title = 'FaceMask'
        self.initUI(thread)

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self, thread):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(1200, 860)
        self.setWindowIcon(QtGui.QIcon("face_chibi.png"))
        self.centralwidget = QWidget(self)
        # create button voice
        self.btn_voice = QPushButton(self.centralwidget)
        self.btn_voice.setGeometry(QRect(1050, 50, 101, 41))
        self.btn_voice.setObjectName("btn_voice")
        self.btn_voice.setText("Start Voice")
        # create icon loading

        # create a label
        self.label = QLabel(self)
        self.label.setGeometry(QRect(40, 40, 960, 720))
        self.label.setMinimumSize(QSize(960, 720))
        self.label.setMaximumSize(QSize(960, 720))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.setStyleSheet("border:0.5px solid #CCC")
        # th = Thread(self)
        self.th = thread
        thread.changePixmap.connect(self.setImage)
        # th.start()
        self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.th.getStatusFromApp(False)
        time.sleep(1)


class LoadingApp(QMainWindow):
    def __init__(self):
        super(LoadingApp, self).__init__()
        self.ui = Ui_LoadingScreen()
        self.ui.setupUi(self)
        self.thread = Thread(self)
        self.thread.start()

        # REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # DROP SHADOW EFFECT
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        # QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(30)
        # CHANGE DESCRIPTION
        # Initial Text
        self.ui.label_description.setText(
            "<strong>WELCOME</strong> TO MY APPLICATION")
        # Change Texts
        QtCore.QTimer.singleShot(4500, lambda: self.ui.label_description.setText(
            "<strong>LOADING</strong> DATABASE"))
        QtCore.QTimer.singleShot(10000, lambda: self.ui.label_description.setText(
            "<strong>LOADING</strong> USER INTERFACE"))
        # SHOW ==> MAIN WINDOW
        self.show()

    # ==> APP FUNCTIONS
    ########################################################################
    def progress(self):
        global counter
        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)
        # CLOSE Loading SCREEN AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()
            # SHOW MAIN WINDOW
            self.main = App(self.thread)
            self.main.show()
            # CLOSE Loading SCREEN
            self.close()
        # INCREASE COUNTER - Config for compatible with loading model
        counter += 0.4


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LoadingApp()
    window.show()
    sys.exit(app.exec_())

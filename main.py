import sys
from PyQt5.QtCore import QThread, pyqtSignal, Qt, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import cv2
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from detection import predict, utils


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    finished = pyqtSignal()

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
            convert_to_qt_format = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_qt_format.scaled(1280, 480, Qt.KeepAspectRatio)
            cv2.waitKey(3)
            self.changePixmap.emit(p)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'FaceMask'
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(800, 800)
        # create a label
        self.label = QLabel(self)
        self.label.move(20, 20)
        self.label.resize(720, 720)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

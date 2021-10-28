from PyQt5.QtCore import (QCoreApplication, QMetaObject,
                          QRect, QSize, Qt)
from PyQt5.QtGui import (QFont,
                         )
from PyQt5.QtWidgets import *


class Loading_CircleBar(object):
    def setupUi(self, LoadingScreen):
        if LoadingScreen.objectName():
            LoadingScreen.setObjectName(u"LoadingScreen")
        LoadingScreen.resize(520, 490)
        self.centralwidget = QWidget(LoadingScreen)
        self.centralwidget.setObjectName("centralwidget")
        self.circularProgressBarBase = QFrame(self.centralwidget)
        self.circularProgressBarBase.setGeometry(
            QRect(50, 30, 411, 411))
        self.circularProgressBarBase.setFrameShape(QFrame.NoFrame)
        self.circularProgressBarBase.setFrameShadow(QFrame.Raised)
        self.circularProgressBarBase.setObjectName("circularProgressBarBase")
        self.circularProgress = QFrame(self.circularProgressBarBase)
        self.circularProgress.setGeometry(QRect(10, 10, 400, 400))
        self.circularProgress.setStyleSheet("QFrame{\n"
                                            "    border-radius: 200px;\n"
                                            "    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:0.749 rgba(255, 0, 127, 0), stop:0.750 rgba(85, 170, 255, 255));\n"
                                            "}")
        self.circularProgress.setFrameShape(QFrame.NoFrame)
        self.circularProgress.setFrameShadow(QFrame.Raised)
        self.circularProgress.setObjectName("circularProgress")
        self.container = QFrame(self.circularProgress)
        self.container.setGeometry(QRect(30, 30, 341, 341))
        self.container.setStyleSheet("QFrame{\n"
                                     "    border-radius: 170px;\n"
                                     "    background-color: rgb(77, 77, 127);\n"
                                     "}")
        self.container.setFrameShape(QFrame.NoFrame)
        self.container.setFrameShadow(QFrame.Raised)
        self.container.setObjectName("container")
        self.layoutWidget = QWidget(self.container)
        self.layoutWidget.setGeometry(QRect(55, 70, 241, 211))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.labelTitle = QLabel(self.layoutWidget)
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.labelTitle.setFont(font)
        self.labelTitle.setStyleSheet("background-color: none;\n"
                                      "color: #FFFFFF")
        self.labelTitle.setAlignment(Qt.AlignCenter)
        self.labelTitle.setObjectName("labelTitle")
        self.gridLayout.addWidget(self.labelTitle, 0, 0, 1, 1)
        self.labelPercentage = QLabel(self.layoutWidget)
        font = QFont()
        font.setFamily("Roboto Thin")
        font.setPointSize(68)
        self.labelPercentage.setFont(font)
        self.labelPercentage.setStyleSheet("background-color: none;\n"
                                           "color: #FFFFFF")
        self.labelPercentage.setAlignment(Qt.AlignCenter)
        self.labelPercentage.setObjectName("labelPercentage")
        self.gridLayout.addWidget(self.labelPercentage, 1, 0, 1, 1)
        self.labelLoadingInfo = QLabel(self.layoutWidget)
        self.labelLoadingInfo.setMinimumSize(QSize(0, 20))
        self.labelLoadingInfo.setMaximumSize(QSize(16777215, 20))
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.labelLoadingInfo.setFont(font)
        self.labelLoadingInfo.setStyleSheet("QLabel{\n"
                                            "    border-radius: 10px;    \n"
                                            "    background-color: rgb(93, 93, 154);\n"
                                            "    color: #FFFFFF;\n"
                                            "    margin-left: 40px;\n"
                                            "    margin-right: 40px;\n"
                                            "}")
        self.labelLoadingInfo.setFrameShape(QFrame.NoFrame)
        self.labelLoadingInfo.setAlignment(Qt.AlignCenter)
        self.labelLoadingInfo.setObjectName("labelLoadingInfo")
        self.gridLayout.addWidget(self.labelLoadingInfo, 2, 0, 1, 1)
        self.labelCredits = QLabel(self.layoutWidget)
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.labelCredits.setFont(font)
        self.labelCredits.setStyleSheet("background-color: none;\n"
                                        "color: rgb(155, 155, 255);")
        self.labelCredits.setAlignment(Qt.AlignCenter)
        self.labelCredits.setObjectName("labelCredits")
        self.gridLayout.addWidget(self.labelCredits, 3, 0, 1, 1)
        self.circularBg = QFrame(self.circularProgressBarBase)
        self.circularBg.setGeometry(QRect(10, 10, 400, 400))
        self.circularBg.setStyleSheet("QFrame{\n"
                                      "    border-radius: 200px;\n"
                                      "    background-color: rgba(77, 77, 127, 120);\n"
                                      "}")
        self.circularBg.setFrameShape(QFrame.NoFrame)
        self.circularBg.setFrameShadow(QFrame.Raised)
        self.circularBg.setObjectName("circularBg")
        self.circularBg.raise_()
        self.circularProgress.raise_()
        LoadingScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoadingScreen)
        QMetaObject.connectSlotsByName(LoadingScreen)
    # setupUi

    def retranslateUi(self, LoadingScreen):
        LoadingScreen.setWindowTitle(QCoreApplication.translate(
            "LoadingScreen", u"MainWindow", None))
        self.labelTitle.setText(QCoreApplication.translate(
            "LoadingScreen", u"<html><head/><body><p><span style=\" font-weight:600; color:#9b9bff;\">FACE MASK DETECTOR</span></p></body></html>", None))
        self.labelPercentage.setText(QCoreApplication.translate(
            "LoadingScreen", u"<p><span style=\" font-size:68pt;\">0</span><span style=\" font-size:58pt; vertical-align:super;\">%</span></p>", None))
        self.labelLoadingInfo.setText(QCoreApplication.translate(
            "LoadingScreen", u"Loading...", None))

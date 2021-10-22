# -*- coding: utf-8 -*-
from PyQt5.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


class Loading_Progressbar(object):
    def setupUi(self, LoadingScreen):
        # Layout
        if LoadingScreen.objectName():
            LoadingScreen.setObjectName(u"LoadingScreen")
        LoadingScreen.resize(680, 400)
        self.centralwidget = QWidget(LoadingScreen)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        # Frame
        self.dropShadowFrame = QFrame(self.centralwidget)
        self.dropShadowFrame.setObjectName(u"dropShadowFrame")
        self.dropShadowFrame.setStyleSheet(u"QFrame {\n"
                                           "	background-color: rgb(56, 58, 89);	\n"
                                           "	color: rgb(220, 220, 220);\n"
                                           "	border-radius: 10px;\n"
                                           "}")
        self.dropShadowFrame.setFrameShape(QFrame.StyledPanel)
        self.dropShadowFrame.setFrameShadow(QFrame.Raised)
        # Title
        self.label_title = QLabel(self.dropShadowFrame)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setGeometry(QRect(0, 90, 661, 61))
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(32)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet(u"color: rgb(254, 121, 199);")
        self.label_title.setAlignment(Qt.AlignCenter)
        # Description
        self.label_description = QLabel(self.dropShadowFrame)
        self.label_description.setObjectName(u"label_description")
        self.label_description.setGeometry(QRect(0, 150, 661, 31))
        font1 = QFont()
        font1.setFamily(u"Segoe UI")
        font1.setPointSize(14)
        self.label_description.setFont(font1)
        self.label_description.setStyleSheet(u"color: rgb(98, 114, 164);")
        self.label_description.setAlignment(Qt.AlignCenter)
        # Progress bar
        self.progressBar = QProgressBar(self.dropShadowFrame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(50, 280, 561, 23))
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
                                       "	\n"
                                       "	background-color: rgb(98, 114, 164);\n"
                                       "	color: rgb(200, 200, 200);\n"
                                       "	border-style: none;\n"
                                       "	border-radius: 10px;\n"
                                       "	text-align: center;\n"
                                       "}\n"
                                       "QProgressBar::chunk{\n"
                                       "	border-radius: 10px;\n"
                                       "	background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(254, 121, 199, 255), stop:1 rgba(170, 85, 255, 255));\n"
                                       "}")
        self.progressBar.setValue(0)
        # Label loading
        self.label_loading = QLabel(self.dropShadowFrame)
        self.label_loading.setObjectName(u"label_loading")
        self.label_loading.setGeometry(QRect(0, 320, 661, 21))
        font2 = QFont()
        font2.setFamily(u"Segoe UI")
        font2.setPointSize(12)
        self.label_loading.setFont(font2)
        self.label_loading.setStyleSheet(u"color: rgb(98, 114, 164);")
        self.label_loading.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.dropShadowFrame)

        LoadingScreen.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoadingScreen)

        QMetaObject.connectSlotsByName(LoadingScreen)

    def retranslateUi(self, SplashScreen):
        SplashScreen.setWindowTitle(QCoreApplication.translate(
            "LoadingScreen", u"MainWindow", None))
        self.label_title.setText(QCoreApplication.translate(
            "LoadingScreen", u"<strong>FACE MASK DETECTOR</strong>", None))
        self.label_description.setText(
            QCoreApplication.translate("LoadingScreen", u"<strong>APP</strong> DESCRIPTION", None))
        self.label_loading.setText(QCoreApplication.translate(
            "LoadingScreen", u"Loading...", None))

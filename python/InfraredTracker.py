# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'python\InfraredTracker.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import os, sys

from PyQt5 import QtCore, QtGui, QtWidgets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ROOT_DIR = os.path.dirname(BASE_DIR)
sys.path.append(BASE_DIR)
# sys.path.append(ROOT_DIR)

from GraphicsView import GraphicsView

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/exchange.png"), QtGui.QIcon.Normal)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        # self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView = GraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout.addWidget(self.horizontalSlider)
        self.labelSlider = QtWidgets.QLabel(self.centralwidget)
        self.labelSlider.setObjectName("labelSlider")
        self.horizontalLayout.addWidget(self.labelSlider)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_2.addWidget(self.checkBox)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.pushButtonLoadVideo = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonLoadVideo.setObjectName("pushButtonLoadVideo")
        self.horizontalLayout_2.addWidget(self.pushButtonLoadVideo)
        self.pushButtonPlay = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonPlay.setObjectName("pushButtonPlay")
        self.horizontalLayout_2.addWidget(self.pushButtonPlay)
        self.horizontalLayout_2.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "目标跟踪"))
        self.labelSlider.setText(_translate("MainWindow", "0/0"))
        self.checkBox.setText(_translate("MainWindow", "跟踪"))
        self.label.setText(_translate("MainWindow", "算法选择:"))
        self.pushButtonLoadVideo.setText(_translate("MainWindow", "加载视频"))
        self.pushButtonPlay.setText(_translate("MainWindow", "开始"))


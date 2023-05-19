# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/zzarryadd/E602B7E902B7BD3D10/Users/Admin/YandexDisk/coding/Hakatons/DB-2023/swan_detector/qt/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from . import resources


class Ui_DetectionWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(811, 608)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setToolTip("")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")
        self.load_button = QtWidgets.QToolButton(self.tab)
        self.load_button.setMinimumSize(QtCore.QSize(300, 300))
        self.load_button.setStyleSheet("")
        self.load_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/download.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.load_button.setIcon(icon)
        self.load_button.setIconSize(QtCore.QSize(64, 64))
        self.load_button.setObjectName("load_button")
        self.gridLayout.addWidget(self.load_button, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.scrollArea = QtWidgets.QScrollArea(self.tab_2)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.list_detections = QtWidgets.QWidget()
        self.list_detections.setGeometry(QtCore.QRect(0, 0, 769, 539))
        self.list_detections.setObjectName("list_detections")
        self.scrollArea.setWidget(self.list_detections)
        self.gridLayout_4.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.reference = QtWidgets.QPlainTextEdit(self.tab_5)
        self.reference.setObjectName("reference")
        self.gridLayout_5.addWidget(self.reference, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_5, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.load_button.setToolTip(_translate("MainWindow", "Загрузить данные для детекции"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Детекция"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "История"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Справка"))

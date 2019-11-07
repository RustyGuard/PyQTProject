# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_evol.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1800, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.spinOverlay = QtWidgets.QSpinBox(self.centralwidget)
        self.spinOverlay.setGeometry(QtCore.QRect(1540, 10, 42, 22))
        self.spinOverlay.setFrame(True)
        self.spinOverlay.setObjectName("spinOverlay")
        self.spinMutationMin = QtWidgets.QSpinBox(self.centralwidget)
        self.spinMutationMin.setGeometry(QtCore.QRect(1540, 40, 42, 22))
        self.spinMutationMin.setFrame(True)
        self.spinMutationMin.setObjectName("spinMutationMin")
        self.spinMutationMax = QtWidgets.QSpinBox(self.centralwidget)
        self.spinMutationMax.setGeometry(QtCore.QRect(1590, 40, 42, 22))
        self.spinMutationMax.setFrame(True)
        self.spinMutationMax.setObjectName("spinMutationMax")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

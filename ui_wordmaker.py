# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_wordmaker.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1067, 683)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.wordStart = QtWidgets.QPushButton(self.centralwidget)
        self.wordStart.setGeometry(QtCore.QRect(600, 290, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(12)
        font.setItalic(False)
        self.wordStart.setFont(font)
        self.wordStart.setObjectName("wordStart")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(600, 20, 351, 211))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(12)
        self.listWidget.setFont(font)
        self.listWidget.setObjectName("listWidget")
        self.b0 = QtWidgets.QPushButton(self.centralwidget)
        self.b0.setGeometry(QtCore.QRect(10, 580, 51, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        self.b0.setFont(font)
        self.b0.setText("")
        self.b0.setObjectName("b0")
        self.b1 = QtWidgets.QPushButton(self.centralwidget)
        self.b1.setGeometry(QtCore.QRect(70, 580, 51, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        self.b1.setFont(font)
        self.b1.setText("")
        self.b1.setObjectName("b1")
        self.b2 = QtWidgets.QPushButton(self.centralwidget)
        self.b2.setGeometry(QtCore.QRect(130, 580, 51, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        self.b2.setFont(font)
        self.b2.setText("")
        self.b2.setObjectName("b2")
        self.b3 = QtWidgets.QPushButton(self.centralwidget)
        self.b3.setGeometry(QtCore.QRect(190, 580, 51, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        self.b3.setFont(font)
        self.b3.setText("")
        self.b3.setObjectName("b3")
        self.b4 = QtWidgets.QPushButton(self.centralwidget)
        self.b4.setGeometry(QtCore.QRect(250, 580, 51, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        self.b4.setFont(font)
        self.b4.setText("")
        self.b4.setObjectName("b4")
        self.b5 = QtWidgets.QPushButton(self.centralwidget)
        self.b5.setGeometry(QtCore.QRect(310, 580, 51, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        self.b5.setFont(font)
        self.b5.setText("")
        self.b5.setObjectName("b5")
        self.b6 = QtWidgets.QPushButton(self.centralwidget)
        self.b6.setGeometry(QtCore.QRect(370, 580, 51, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        self.b6.setFont(font)
        self.b6.setText("")
        self.b6.setObjectName("b6")
        self.turnCancel = QtWidgets.QPushButton(self.centralwidget)
        self.turnCancel.setEnabled(False)
        self.turnCancel.setGeometry(QtCore.QRect(780, 350, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(12)
        self.turnCancel.setFont(font)
        self.turnCancel.setObjectName("turnCancel")
        self.turnEnd = QtWidgets.QPushButton(self.centralwidget)
        self.turnEnd.setGeometry(QtCore.QRect(600, 350, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(12)
        self.turnEnd.setFont(font)
        self.turnEnd.setObjectName("turnEnd")
        self.wordX = QtWidgets.QSpinBox(self.centralwidget)
        self.wordX.setGeometry(QtCore.QRect(610, 240, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(12)
        self.wordX.setFont(font)
        self.wordX.setMaximum(15)
        self.wordX.setObjectName("wordX")
        self.wordY = QtWidgets.QSpinBox(self.centralwidget)
        self.wordY.setGeometry(QtCore.QRect(680, 240, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(12)
        self.wordY.setFont(font)
        self.wordY.setMaximum(15)
        self.wordY.setObjectName("wordY")
        self.wordLen = QtWidgets.QSpinBox(self.centralwidget)
        self.wordLen.setGeometry(QtCore.QRect(750, 240, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(12)
        self.wordLen.setFont(font)
        self.wordLen.setMinimum(1)
        self.wordLen.setMaximum(16)
        self.wordLen.setObjectName("wordLen")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(820, 240, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.wordEnd = QtWidgets.QPushButton(self.centralwidget)
        self.wordEnd.setEnabled(False)
        self.wordEnd.setGeometry(QtCore.QRect(780, 290, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(12)
        self.wordEnd.setFont(font)
        self.wordEnd.setObjectName("wordEnd")
        self.cursorLet = QtWidgets.QLabel(self.centralwidget)
        self.cursorLet.setEnabled(True)
        self.cursorLet.setGeometry(QtCore.QRect(430, 580, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(16)
        self.cursorLet.setFont(font)
        self.cursorLet.setText("")
        self.cursorLet.setObjectName("cursorLet")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1067, 21))
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
        self.wordStart.setText(_translate("MainWindow", "Начать ввод"))
        self.turnCancel.setText(_translate("MainWindow", "Отменить слово"))
        self.turnEnd.setText(_translate("MainWindow", "Закончить ход"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Горизонтально"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Вертикально"))
        self.wordEnd.setText(_translate("MainWindow", "Закончить слово"))

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
        MainWindow.resize(1530, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(1040, 10, 441, 261))
        self.tabWidget.setObjectName("tabWidget")
        self.page0 = QtWidgets.QWidget()
        self.page0.setObjectName("page0")
        self.tabWidget.addTab(self.page0, "")
        self.page1 = QtWidgets.QWidget()
        self.page1.setObjectName("page1")
        self.tabWidget.addTab(self.page1, "")
        self.page2 = QtWidgets.QWidget()
        self.page2.setObjectName("page2")
        self.comboGen = QtWidgets.QComboBox(self.page2)
        self.comboGen.setGeometry(QtCore.QRect(10, 10, 171, 31))
        self.comboGen.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboGen.setObjectName("comboGen")
        self.spinMutChance = QtWidgets.QSpinBox(self.page2)
        self.spinMutChance.setGeometry(QtCore.QRect(10, 50, 51, 31))
        self.spinMutChance.setMaximum(100)
        self.spinMutChance.setProperty("value", 25)
        self.spinMutChance.setObjectName("spinMutChance")
        self.spinMutTimes = QtWidgets.QSpinBox(self.page2)
        self.spinMutTimes.setGeometry(QtCore.QRect(70, 50, 51, 31))
        self.spinMutTimes.setMinimum(1)
        self.spinMutTimes.setMaximum(30)
        self.spinMutTimes.setProperty("value", 3)
        self.spinMutTimes.setObjectName("spinMutTimes")
        self.boxDouble = QtWidgets.QCheckBox(self.page2)
        self.boxDouble.setGeometry(QtCore.QRect(10, 90, 111, 21))
        self.boxDouble.setFocusPolicy(QtCore.Qt.NoFocus)
        self.boxDouble.setChecked(True)
        self.boxDouble.setObjectName("boxDouble")
        self.boxMulti = QtWidgets.QCheckBox(self.page2)
        self.boxMulti.setGeometry(QtCore.QRect(10, 120, 111, 21))
        self.boxMulti.setFocusPolicy(QtCore.Qt.NoFocus)
        self.boxMulti.setChecked(True)
        self.boxMulti.setObjectName("boxMulti")
        self.tabWidget.addTab(self.page2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1530, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.page0), _translate("MainWindow", "Enegry"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.page1), _translate("MainWindow", "Minerals"))
        self.spinMutChance.setToolTip(_translate("MainWindow", "Шанс мутации в %"))
        self.spinMutTimes.setToolTip(_translate("MainWindow", "Количество мутаций"))
        self.boxDouble.setText(_translate("MainWindow", "Разделение"))
        self.boxMulti.setText(_translate("MainWindow", "Увеличение"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.page2), _translate("MainWindow", "Genoms"))

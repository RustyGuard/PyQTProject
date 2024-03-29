import random
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication

from Evolution.cell import commands, Cell
from Evolution.world import World
from ui_evol import Ui_MainWindow
from game import Game


class Evolution(Game, Ui_MainWindow):
    def __init__(self, parent):
        self.speeds = [60.0, 1.5, 1.0, 0.5, 0.25, 0.15, 0.05]
        self.speed = 2
        super().__init__(parent, 1000 * self.speeds[self.speed] // 60)
        self.world = World(100, 85)
        self.paused = True
        self.updateComboBox()
        self.comboGen.currentTextChanged.connect(self.itemChanged)
        self.tabWidget.currentChanged.connect(self.overlayChange)
        self.spinMutChance.valueChanged.connect(self.mutationChange)
        self.spinMutTimes.valueChanged.connect(self.mutationChange)
        self.boxDouble.stateChanged.connect(self.mutationChange)
        self.boxMulti.stateChanged.connect(self.mutationChange)
        self.boxX.setMaximum(self.world.width - 1)
        self.boxY.setMaximum(self.world.height - 1)
        self.boxX.valueChanged.connect(self.updateSelected)
        self.boxY.valueChanged.connect(self.updateSelected)
        self.btnUpdateCell.clicked.connect(self.updateSelected)
        self.updateSelected()
        self.updateInsertComboBox()
        self.changeGen.clicked.connect(self.insertIntoGenom)
        self.scaleMin.valueChanged.connect(self.updateScales)
        self.scaleEn.valueChanged.connect(self.updateScales)

    def updateScales(self):
        World.scale_minerals = self.scaleMin.value()
        World.scale_energy = self.scaleEn.value()

    def updateSelected(self):
        World.curr_x = self.boxX.value()
        World.curr_y = self.boxY.value()
        cell = self.world.getCell(World.curr_x, World.curr_y)
        self.listGenom.clear()
        if cell is None:
            return
        for cmd in cell.genom:
            self.listGenom.addItem(commands.cmd_list[cmd][1])
        self.currInfo.setText(f'Здоровье: {cell.health}\nМинералы: {cell.mineral}')

    def insertIntoGenom(self):
        index = self.listGenom.currentRow()
        if index == -1 or not self.paused:
            return
        cell = self.world.getCell(World.curr_x, World.curr_y)
        cell.genom[index] = self.comboGenChange.currentIndex()
        self.updateSelected()

    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_S:
            self.speed = (self.speed + 1) % len(self.speeds)
            print(f'Speed is: {self.speeds[self.speed]}')
            self.killTimer(self.updateTimer)
            self.updateTimer = self.startTimer(int(1000 * self.speeds[self.speed]) // 60)
            return
        if e.key() == Qt.Key_Space:
            self.paused = not self.paused
            return
        fs = [Qt.Key_F1, Qt.Key_F2, Qt.Key_F3, Qt.Key_F4, Qt.Key_F5, Qt.Key_F6, Qt.Key_F7, Qt.Key_F8, Qt.Key_F9,
              Qt.Key_F10, Qt.Key_F11, Qt.Key_F12]
        if e.key() in fs:
            World.overlay = fs.index(e.key())
            self.tabWidget.setCurrentIndex(World.overlay)

    def mutationChange(self):
        Cell.mutChance = self.spinMutChance.value()
        Cell.mutTimes = self.spinMutTimes.value()
        Cell.doubling = self.boxDouble.isChecked()
        Cell.multing = self.boxMulti.isChecked()

    def overlayChange(self):
        World.overlay = self.tabWidget.currentIndex()

    def updateComboBox(self):
        self.comboGen.clear()
        for i in commands.cmd_groups:
            self.comboGen.addItem(i)

    def updateInsertComboBox(self):
        self.comboGenChange.clear()
        for i in commands.cmd_list:
            self.comboGenChange.addItem(i[1])

    def itemChanged(self):
        World.curr_gen = self.comboGen.currentText()

    def OnUpdate(self, delta):
        if not self.paused:
            self.world.update()

    def paintEvent(self, e):
        qp = QPainter(self)
        self.world.draw(qp)


if __name__ == '__main__':
    a = QApplication(sys.argv)
    ex = Evolution(None)
    ex.show()
    sys.exit(a.exec_())

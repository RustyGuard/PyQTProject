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
        self.speeds = [0.05, 0.25, 0.5, 1.0, 1.5, 60.0]
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
        for i in commands.cmd_groups:
            self.comboGen.addItem(i)

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

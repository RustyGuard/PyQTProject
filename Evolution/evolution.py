import random
import sys

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication

from Evolution.world import World
from ui_evol import Ui_MainWindow
from game import Game


class Evolution(Game, Ui_MainWindow):
    def __init__(self, parent):
        super().__init__(parent, 1000 // 120)
        self.spinOverlay.valueChanged.connect(self.overlayChange)
        self.spinMutationMin.valueChanged.connect(self.mutationChange)
        self.spinMutationMax.valueChanged.connect(self.mutationChange)
        self.world = World(100, 100)

    def overlayChange(self):
        World.overlay = self.spinOverlay.value()

    def mutationChange(self):
        World.find_gen_min = self.spinMutationMin.value()
        World.find_gen_max = self.spinMutationMax.value()

    def OnUpdate(self, delta):
        self.world.update()

    def paintEvent(self, e):
        qp = QPainter(self)
        self.world.draw(qp)


if __name__ == '__main__':
    a = QApplication(sys.argv)
    ex = Evolution(None)
    ex.show()
    sys.exit(a.exec_())

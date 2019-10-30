import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QApplication

from ui_snake import Ui_MainWindow
from game import Game
import random


class SnakeWindow(Game, Ui_MainWindow):
    def __init__(self, parent):
        super().__init__(parent, 200)
        print('Snake!')
        self.locked = False
        self.GRID_SIZE = 20
        self.dir = 0
        self.direction = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        self.grid = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]
        self.grid[5][5] = 1
        self.grid[0][1] = -1
        self.snake_info = [5, 5, 1]
        self.colors = {
            'nothing': QColor(125, 125, 125),
            'fruit': QColor(255, 100, 100),
            'body': QColor(100, 200, 100),
            'head': QColor(0, 200, 0)
        }
        for i, btn in enumerate([self.btn0, self.btn1, self.btn2, self.btn3]):
            btn.direction = i
            btn.clicked.connect(self.twist)

    def gen_fruit(self):
        x, y = random.randint(0, self.GRID_SIZE - 1), random.randint(0, self.GRID_SIZE - 1)
        while self.grid[x][y] != 0:
            x, y = random.randint(0, self.GRID_SIZE - 1), random.randint(0, self.GRID_SIZE - 1)
        self.grid[x][y] = -1

    def get_tile(self, x, y, default=-2):
        if 0 <= x < self.GRID_SIZE and 0 <= y < self.GRID_SIZE:
            return self.grid[x][y]
        return default

    # Return last tile value
    def move_snake(self):
        dir = self.direction[self.dir]
        self.snake_info[0] += dir[0]
        self.snake_info[1] += dir[1]
        tile = self.get_tile(self.snake_info[0], self.snake_info[1])
        if tile != -2:
            self.grid[self.snake_info[0]][self.snake_info[1]] = self.snake_info[2] + 1
        return tile

    def twist(self):
        self.dir = self.sender().direction
        self.updateLabel()

    def updateLabel(self):
        arrows = ['↑', '→', '↓', '←']
        self.label.setText(arrows[self.dir])

    def keyPressEvent(self, e):
        keys = [Qt.Key_W, Qt.Key_D, Qt.Key_S, Qt.Key_A]
        try:
            index = keys.index(e.key())
        except ValueError:
            index = -1
        if index != -1:
            if self.locked and (self.dir + index) % 2 == 0:
                print('Sorry it is locked')
                return
            self.dir = index
            self.updateLabel()
        if e.key() == Qt.Key_L:
            self.locked = not self.locked
            print(self.locked)
            if self.locked:
                self.label_2.setText('🔐')
            else:
                self.label_2.setText('🔓')

    def OnUpdate(self, delta):
        tile = self.move_snake()
        if tile > 0 or tile == -2:
            print('Game over')
            QMessageBox.about(self, 'Game over', 'Поражение')
            self.grid = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]
            self.grid[5][5] = 1
            self.snake_info = [5, 5, 1]
            self.gen_fruit()
            return
        elif tile == -1:
            self.snake_info[2] += 1
            self.gen_fruit()
        else:
            for x in range(self.GRID_SIZE):
                for y in range(self.GRID_SIZE):
                    if self.grid[x][y] > 0:
                        self.grid[x][y] -= 1

    def paintEvent(self, e):
        qp = QPainter(self)
        cell_size = 500 / self.GRID_SIZE
        for x in range(self.GRID_SIZE):
            for y in range(self.GRID_SIZE):
                if x == self.snake_info[0] and y == self.snake_info[1]:
                    qp.fillRect(x * (cell_size + 1), y * (cell_size + 1), cell_size, cell_size, self.colors['head'])
                    continue
                tile = self.grid[x][y]
                if tile == 0:
                    qp.fillRect(x * (cell_size + 1), y * (cell_size + 1), cell_size, cell_size, self.colors['nothing'])
                elif tile == -1:
                    qp.fillRect(x * (cell_size + 1), y * (cell_size + 1), cell_size, cell_size, self.colors['fruit'])
                else:
                    qp.fillRect(x * (cell_size + 1), y * (cell_size + 1), cell_size, cell_size, self.colors['body'])

    def getName(self):
        return 'Snake'


if __name__ == '__main__':
    a = QApplication(sys.argv)
    ex = SnakeWindow(None)
    ex.show()
    sys.exit(a.exec_())
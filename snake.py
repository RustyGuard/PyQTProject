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
        self.locked = True
        self.GRID_SIZE = 20
        self.direction = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        self.new_snake()
        self.last = 0
        self.paused = True
        self.colors = {
            'nothing': QColor(125, 125, 125),
            'fruit': QColor(255, 75, 75)
        }

    def gen_fruit(self):
        x, y = random.randint(0, self.GRID_SIZE - 1), random.randint(0, self.GRID_SIZE - 1)
        while self.grid[x][y] != 0:
            x, y = random.randint(0, self.GRID_SIZE - 1), random.randint(0, self.GRID_SIZE - 1)
        self.grid[x][y] = -1

    def get_tile(self, x, y, default=-2):
        if 0 <= x < self.GRID_SIZE and 0 <= y < self.GRID_SIZE:
            return self.grid[x][y]
        return default

    def new_snake(self):
        self.paused = True
        self.grid = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]
        self.dir = 0
        self.grid[self.GRID_SIZE // 2][self.GRID_SIZE // 2] = 4
        self.snake_info = [self.GRID_SIZE // 2, self.GRID_SIZE // 2, 4]
        self.gen_fruit()

    # Return last tile value
    def move_snake(self):
        self.last = self.dir
        dir = self.direction[self.dir]
        self.snake_info[0] += dir[0]
        self.snake_info[1] += dir[1]
        tile = self.get_tile(self.snake_info[0], self.snake_info[1])
        if tile != -2:
            self.grid[self.snake_info[0]][self.snake_info[1]] = self.snake_info[2] + 1
        return tile

    def updateLabel(self):
        arrows = ['↑', '→', '↓', '←']
        self.label.setText(arrows[self.dir])

    def keyPressEvent(self, e):
        keys = [[Qt.Key_W, Qt.Key_Up], [Qt.Key_D, Qt.Key_Right], [Qt.Key_S, Qt.Key_Down], [Qt.Key_A, Qt.Key_Left]]
        index = -1
        for i, key in enumerate(keys):
            if e.key() in key:
                index = i
        if index != -1:
            if self.locked and (self.last + index) % 2 == 0 and self.last != index:
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
        elif e.key() == Qt.Key_Space:
            self.paused = not self.paused
            return
        self.paused = False

    def OnUpdate(self, delta):
        if self.paused:
            return
        tile = self.move_snake()
        if tile > 0 or tile == -2:
            print('Game over')
            QMessageBox.about(self, 'Game over', 'Поражение')
            self.new_snake()
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
        cell_size = 500 // self.GRID_SIZE
        for x in range(self.GRID_SIZE):
            for y in range(self.GRID_SIZE):
                tile = self.grid[x][y]
                if tile == 0:
                    self.rectangle(qp, x * cell_size, y * cell_size, cell_size, cell_size, self.colors['nothing'])
                elif tile == -1:
                    self.rectangle(qp, x * cell_size, y * cell_size, cell_size, cell_size, self.colors['fruit'])
                else:
                    g = tile * 255 // self.snake_info[2] // 2 + 125
                    self.rectangle(qp, x * cell_size, y * cell_size, cell_size, cell_size, QColor(0, g, 0))

    def getName(self):
        return 'Snake'

    def rectangle(self, qp, x, y, width, height, color):
        qp.fillRect(x, y, width, height, color)
        qp.drawRect(x, y, width, height)


if __name__ == '__main__':
    a = QApplication(sys.argv)
    ex = SnakeWindow(None)
    ex.show()
    sys.exit(a.exec_())

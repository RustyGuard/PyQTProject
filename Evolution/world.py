from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush, QPen

from Evolution.cell import Cell


class Overlay:
    def draw(self, world, qp):
        pass

    def get_color(self, cell):
        return QColor(0, 0, 0)


class EnergyOverlay(Overlay):
    def draw(self, world, qp):
        for i in range(world.height):
            sun = max(23 * (11 - (15 * i / world.height)), 0)
            qp.fillRect(0, i * world.cell_size, world.cell_size * world.width, world.cell_size * world.height,
                        QColor(sun, sun, sun / 2))

    def get_color(self, cell):
        en = min(cell.health * 255 / 1000, 255)
        return QColor(en, en, 45)


class GenOverlay(Overlay):
    def get_color(self, cell):
        g = cell.genom.count(World.find_gen_min) * 255 // len(cell.genom)
        return QColor(100, g, 100) if g > 0 else Qt.black


class MineralOverlay(Overlay):
    def draw(self, world, qp):
        for i in range(world.height):
            mineral = 0
            if i > world.height // 2:
                mineral += 1
            if i > world.height // 6 * 4:
                mineral += 1
            if i > world.height // 6 * 5:
                mineral += 1
            qp.fillRect(0, i * world.cell_size, world.cell_size * world.width, world.cell_size * world.height,
                        QColor(0, 0, 85 * mineral))

    def get_color(self, cell):
        m = min(cell.mineral * 255 / 1000, 255)
        return QColor(25, 25, m)


class World:
    overlay = 0
    find_gen_min = 0
    find_gen_max = 0

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.grid = [[None] * height for _ in range(width)]
        self.cell_size = 10
        self.pause = False
        self.cells = []
        self.setCell(width // 2 - 1, height // 6, Cell(self, width // 2 - 1, height // 6))
        self.overlays = []
        self.overlays.append(EnergyOverlay())
        self.overlays.append(MineralOverlay())
        self.overlays.append(GenOverlay())

    def setCell(self, x, y, cell):
        if not self.isValid(x, y):
            return
        if self.grid[x][y] is not None:
            self.cells.remove(self.grid[x][y])
        self.grid[x][y] = cell
        self.cells.append(cell)

    def isValid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def getCell(self, x, y):
        if not self.isValid(x, y):
            return None
        return self.grid[x][y]

    def isEmpty(self, x, y):
        if self.isValid(x, y):
            if self.grid[x][y] is None:
                return True
        return False

    def deleteCell(self, cell):
        self.grid[cell.x][cell.y] = None
        self.cells.remove(cell)
        if cell.mprev is not None:
            cell.mprev.mnext = None
        if cell.mnext is not None:
            cell.mnext.mprev = None
        cell.mprev = None
        cell.mnext = None

    def moveCell(self, x, y, cell):
        if (not self.isEmpty(x, y)) or cell.isMulti() != 0:
            return
        self.grid[x][y] = cell
        self.grid[cell.x][cell.y] = None
        cell.x = x
        cell.y = y

    def update(self):
        for cell in self.cells:
            cell.think()

    def draw(self, qp):
        qp.fillRect(0, 0, self.width * self.cell_size, self.height * self.cell_size, QColor(200, 200, 200))
        dead_pen = QPen(QColor(255, 0, 0), 2, Qt.SolidLine)
        alive_pen = QPen(QColor(125, 125, 125), 1, Qt.SolidLine)
        self.overlays[World.overlay].draw(self, qp)
        for i in self.cells:
            qp.setBrush(self.overlays[World.overlay].get_color(i))
            qp.setPen(dead_pen if i.dead else alive_pen)
            qp.drawRect(i.x * self.cell_size, i.y * self.cell_size, self.cell_size, self.cell_size)

from PyQt5.QtGui import QColor

from Evolution.cell import Cell


class Overlay:
    def draw(self, qp):
        pass

    def get_color(self, cell):
        return QColor(0, 0, 0)


class EnergyOverlay(Overlay):
    def get_color(self, cell):
        en = min(cell.health * 255 / 1000, 255)
        if cell.dead:
            return QColor(en // 2 + 125, 0, 0)
        return QColor(en, en, 45)


class World:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.grid = [[None] * height for _ in range(width)]
        self.cell_size = 10
        self.pause = False
        self.cells = []
        self.setCell(width // 2 - 1, height // 2 - 1, Cell(self, width // 2 - 1, height // 2 - 1))
        self.overlays = []
        self.overlays.append(EnergyOverlay())

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
        self.grid[cell.getX()][cell.getY()] = None
        self.cells.remove(cell)
        if cell.mprev is not None:
            cell.mprev.mnext = None
        if cell.mnext is not None:
            cell.mnext.mprev = None;
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
        for i in self.cells:
            qp.fillRect(i.x * self.cell_size, i.y * self.cell_size, self.cell_size, self.cell_size, self.overlays[0]
                        .get_color(i))

import random

commands = []


def add_command(cmd):
    commands.append(cmd)


# Function must return another
def add_command_i(cmd, index):
    for i in range(index):
        commands.append(cmd(i))


def move_i(i):
    def move(cell):
        xt = cell.xFromDirectionA(i)
        yt = cell.yFromDirectionA(i)
        cell.world.moveCell(xt, yt, cell)
        return True
    return move


def photosynthesis(cell):
    cell.health += 50
    return True


add_command(photosynthesis)
add_command_i(move_i, 8)


class Cell:
    def __init__(self, world, x, y, genom=None):
        self.dead = False
        self.world = world
        self.x, self.y = x, y
        self.health = 150
        self.genom = [0] * 30 if genom is None else genom.copy()
        world.setCell(x, y, self)
        self.task = 0

    def think(self):
        if self.dead:
            return
        for _ in range(15):
            if commands[self.genom[self.task]](self):
                self.nextTask()
                break
        self.health -= 3
        if self.health <= 0:
            self.dead = True
        if self.health > 999:
            self.cellDouble()
            self.health -= 150

    def mutate(self, chance, times):
        if random.randint(0, 100) < chance:
            for _ in range(times):
                self.genom[random.randint(0, len(self.genom) - 1)] = random.randint(0, len(commands) - 1)

    def nextTask(self, i=1):
        self.task += i
        self.task = self.task % len(self.genom)

    def xFromDirectionA(self, dir):
        xt = self.x
        if dir in [0, 6, 7]:
            xt = xt - 1
        if dir in [2, 3, 4]:
            xt = xt + 1
        if xt == -1:
            xt = self.world.width - 1
        if xt == self.world.width:
            xt = 0
        return xt

    def yFromDirectionA(self, dir):
        yt = self.y
        if dir in [0, 1, 2]:
            yt = yt - 1
        elif dir in [4, 5, 6]:
            yt = yt + 1
        return yt

    def findEmptyDirection(self):
        for i in range(8):
            xt = self.xFromDirectionA(i)
            yt = self.yFromDirectionA(i)
            if self.world.isEmpty(xt, yt):
                return i
        return 8

    def cellDouble(self):
        dir = self.findEmptyDirection()
        if dir == 8:
            self.dead = True
            return
        baby = Cell(self.world, self.xFromDirectionA(dir), self.yFromDirectionA(dir), self.genom)
        baby.health = self.health // 2
        self.health = self.health // 2
        baby.mutate(100, 30)

    def isMulti(self):
        return 0

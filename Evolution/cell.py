import random

commands = []


def add_command(cmd):
    commands.append(cmd)
    print(len(commands))


# Function must return another
def add_command_i(cmd, index):
    for i in range(index):
        commands.append(cmd(i))
    print(len(commands))


def move_i(i):
    def move(cell):
        xt = cell.xFromDirectionA(i)
        yt = cell.yFromDirectionA(i)
        cell.world.moveCell(xt, yt, cell)
        return True
    return move


def photosynthesis(cell):
    if cell.mineral < 100:
        t = 0
    elif cell.mineral < 400:
        t = 1
    else:
        t = 2
    a = 0
    if cell.mnext is not None:
        a += 2
    if cell.mprev is not None:
        a += 2
    hl = a + 1 * (11 - (15 * cell.y / cell.world.height) + t)
    if hl > 0:
        cell.health += int(hl)
    return True


def eat_i(i):
    def eat(cell):
        cell.eat(i)
        return True
    return eat


def mineral_to_energy(cell):
    if cell.mineral > 0:
        print(cell.mineral)
    if cell.mineral > 50:
        cell.health += 150
        cell.mineral -= 50
    else:
        cell.health += cell.mineral * 3
        cell.mineral = 0


add_command(photosynthesis)
add_command_i(move_i, 8)
add_command_i(eat_i, 8)
add_command(mineral_to_energy)
add_command(mineral_to_energy)


class Cell:
    def __init__(self, world, x, y, genom=None):
        self.dead = False
        self.world = world
        self.x, self.y = x, y
        self.health = 150
        self.mineral = 0
        self.genom = [0] * 30 if genom is None else genom.copy()
        world.setCell(x, y, self)
        self.task = 0
        self.mprev = None
        self.mnext = None

    def think(self):
        if self.dead:
            return
        for _ in range(15):
            if commands[self.genom[self.task]](self):
                self.nextTask()
                break
        self.health -= 3
        if self.health > 999:
            self.cellDouble()
            self.health -= 150

        if self.y > self.world.height / 2:
            self.mineral += 1
        if self.y > self.world.height / 6 * 4:
            self.mineral += 1
        if self.y > self.world.height / 6 * 5:
            self.mineral += 1
        if self.mineral > 999:
            self.mineral = 999

        if self.health <= 0:
            self.dead = True
            self.health = 300

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
        baby.mutate(75, 3)

    def eat(self, dir):
        xt = self.xFromDirectionA(dir)
        yt = self.yFromDirectionA(dir)
        cell = self.world.getCell(xt, yt)
        if cell is None:
            return
        if cell.dead:
            self.health += 100
            self.world.deleteCell(cell)
            # print('Organic eaten.')
            return
        if self.mineral >= cell.mineral:
            self.mineral -= cell.mineral
            self.health += (100 + cell.health // 2)
            self.world.deleteCell(cell)
            # print('Had more minerals and bite.')
            return
        cell.mineral -= self.mineral
        self.mineral = 0
        if self.health > cell.mineral * 2:
            self.mineral -= cell.mineral
            self.health += (100 + (cell.health / 2))
            self.world.deleteCell(cell)
            # print('Had less minerals and bite.')
            return
        # print('Had less and dead')
        self.world.deleteCell(self)

    def isMulti(self):
        return 0

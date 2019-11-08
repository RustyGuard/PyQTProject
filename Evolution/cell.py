import random


class CommandList:
    def __init__(self):
        self.cmd_list = []
        self.cmd_groups = {}
        self.sum_chance = 0

    def __getitem__(self, item):
        return self.cmd_list[item][0]

    def __len__(self):
        return len(self.cmd_list)

    def add_command(self, chance, cmd, desc):
        self.cmd_list.append((cmd, desc))
        self.cmd_groups[desc] = (chance, [len(self) - 1])
        print('Before', self.sum_chance)
        self.sum_chance += chance
        print('After', self.sum_chance)

    def add_dir_command(self, chance, cmd, desc):
        ids = []
        symb = ['↖', '↑', '↗', '→', '↘', '↓', '↙', '←']
        for i, s in enumerate(symb):
            self.cmd_list.append((cmd(i), desc + symb[i]))
            ids.append(len(self) - 1)
        self.cmd_groups[desc] = (chance, ids)
        print('Before', self.sum_chance)
        self.sum_chance += chance
        print('After', self.sum_chance)

    def get_random(self):
        num = random.randint(0, self.sum_chance - 1)
        for i in self.cmd_groups:
            num -= self.cmd_groups[i][0]
            if num < 0:
                return random.choice(self.cmd_groups[i][1])
        print(f'Random is wrong! {num} of {self.sum_chance}')
        return 0


def move_i(i):
    def move(cell):
        xt = cell.xFromDirectionR(i)
        yt = cell.yFromDirectionR(i)
        cell.world.moveCell(xt, yt, cell)
        cell.health -= 3
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
    if cell.mineral > 50:
        cell.health += 150
        cell.mineral -= 50
    else:
        cell.health += cell.mineral * 3
        cell.mineral = 0
    return True


def is_friend_i(i):
    def is_friend(cell):
        xt = cell.xFromDirectionR(i)
        yt = cell.yFromDirectionR(i)
        c = cell.world.getCell(xt, yt)
        if c is None:
            cell.nextTask(3)
            return False
        if c == cell.mprev or c == cell.mnext:
            cell.nextTask(2)
            return False
        cell.nextTask(1)
        return False
    return is_friend


commands = CommandList()
commands.add_command(12, photosynthesis, 'Gen energy from sun.')
commands.add_dir_command(10, move_i, 'Move')
commands.add_dir_command(5, eat_i, 'Eat')
commands.add_command(2, mineral_to_energy, 'Convert minerals to sun.')
commands.add_dir_command(3, is_friend_i, 'Check cell.')


class Cell:
    mutChance = 25
    mutTimes = 3
    doubling = True
    multing = True

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
        self.dir = random.randint(0, 7)

    def think(self):
        if self.dead:
            return
        for _ in range(15):
            if commands[self.genom[self.task]](self):
                self.nextTask()
                break
        if self.health > 999:
            if self.isMulti() == 3:
                if Cell.doubling:
                    self.cellDouble()
                    self.health -= 150
            else:
                if Cell.multing:
                    self.cellMulti()
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
            self.cell2Organic()
            # print('Hunger')
            self.health = 300

        a = self.isMulti()
        if a == 3:
            m = self.mineral + self.mprev.mineral + self.mnext.mineral
            m = m / 3
            self.mineral = m
            self.mnext.mineral = m
            self.mprev.mineral = m
            if self.mprev.isMulti() == 3 and self.mnext.isMulti() == 3:
                h = self.health + self.mprev.health + self.mnext.health
                h = h / 3
                self.health = h
                self.mnext.health = h
                self.mprev.health = h
        elif a != 0:
            b = None
            if a == 1:
                b = self.mprev
            if a == 2:
                b = self.mnext
            ab = b.isMulti()
            if ab == 3:
                h = self.health + b.health
                h = h / 6
                self.health = h * 5
                b.health = h

    def mutate(self):
        if random.randint(0, 99) < Cell.mutChance:
            for _ in range(Cell.mutTimes):
                self.genom[random.randint(0, len(self.genom) - 1)] = commands.get_random()

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

    def xFromDirectionR(self, dir):
        dir += self.dir
        if dir >= 8:
            dir -= 8
        return self.xFromDirectionA(dir)

    def yFromDirectionR(self, dir):
        dir += self.dir
        if dir >= 8:
            dir -= 8
        return self.yFromDirectionA(dir)

    def findEmptyDirection(self):
        for i in random.sample(range(8), 8):
            xt = self.xFromDirectionR(i)
            yt = self.yFromDirectionR(i)
            if self.world.isEmpty(xt, yt):
                return i
        return 8

    def cell2Organic(self):
        self.dead = True
        if self.mnext is not None:
            self.mnext.mprev = None
            self.mnext = None
        if self.mprev is not None:
            self.mprev.mnext = None
            self.mprev = None

    def cellDouble(self):
        dir = self.findEmptyDirection()
        if dir == 8:
            self.cell2Organic()
            return
        baby = Cell(self.world, self.xFromDirectionR(dir), self.yFromDirectionR(dir), self.genom)
        baby.health = self.health // 2
        self.health = self.health // 2
        baby.mutate()

    def cellMulti(self):
        if (self.mprev is not None) and (self.mnext is not None):
            return
        dir = self.findEmptyDirection()
        if dir == 8:
            # print('Death')
            self.cell2Organic()
            return
        xt = self.xFromDirectionR(dir)
        yt = self.yFromDirectionR(dir)
        baby = Cell(self.world, xt, yt, self.genom)
        baby.mutate()
        baby.health = self.health // 2
        self.health = self.health // 2
        # b.direction = (int)(Math.random() * 4)
        if self.mnext is None:
            self.mnext = baby
            baby.mprev = self
        else:
            self.mprev = baby
            baby.mnext = self

    def eat(self, dir):
        xt = self.xFromDirectionR(dir)
        yt = self.yFromDirectionR(dir)
        cell = self.world.getCell(xt, yt)
        if cell is None:
            return
        # if cell == self.mprev or cell == self.mnext:
            # return
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
        a = 0
        if self.mprev is not None:
            a = 1
        if self.mnext is not None:
            a = a + 2
        return a

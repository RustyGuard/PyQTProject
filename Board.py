import sqlite3
import pymorphy2
import random

from PyQt5.QtGui import QColor, QPainter


def get_x(x, offset, hor):
    if hor:
        return x + offset
    else:
        return x


def get_y(y, offset, hor):
    if hor:
        return y
    else:
        return y + offset


class Board:
    def __init__(self, log):
        self.let_con = sqlite3.connect('res/letters.db')
        self.morph = pymorphy2.MorphAnalyzer()
        self.words = []
        self.log = log

    def generate(self):
        self.grid = [[''] * 16 for _ in range(16)]
        self.chips = []
        cur = self.let_con.cursor()
        for i in cur.execute('''SELECT * FROM letters''').fetchall():
            for j in range(i[2]):
                self.chips.append(i[1])
        self.chips = random.sample(self.chips, len(self.chips))
        # 1 - x2 for letter
        # 2 - x3 for letter
        # 3 - x2 for word
        # 4 - x3 for word
        # 5 - Cell for first word
        # TODO Move to other file
        self.boosters = {
            (3, 0): 1,
            (0, 3): 1,
            (1, 6): 2,
            (6, 1): 2,
            (10, 1): 2,
            (1, 10): 2,
            (1, 1): 3,
            (2, 2): 3,
            (0, 0): 4,
            (15, 0): 4,
            (0, 15): 4,
            (15, 15): 4,
            (8, 0): 4,
            (0, 8): 4,
            (8, 15): 4,
            (15, 8): 4,
            (7, 7): 5,
            (7, 8): 5,
            (8, 7): 5,
            (8, 8): 5
        }
        self.boost_colors = {
            1: QColor(125, 255, 125),
            2: QColor(255, 255, 0),
            3: QColor(125, 125, 255),
            4: QColor(255, 125, 125),
            5: QColor(255, 179, 0)
        }

    def draw_boosters(self, qp):
        for i in self.boosters:
            qp.setBrush(self.boost_colors[self.boosters[i]])
            qp.drawRect(i[0] * 36 - 1, i[1] * 36 - 1, 36, 36)

    def take_chip(self):
        return self.chips.pop(-1)

    def next_chips(self):
        if len(self.chips) < 7:
            self.curr_chips = [''] * 7
        else:
            self.curr_chips = [self.take_chip() for _ in range(7)]

    def update_chips(self, btns):
        for i, btn in zip(self.curr_chips, btns):
            btn.setText(i)
            if i != '':
                btn.setToolTip(f'Очков за букву: {self.get_letter_value(i)}')
            else:
                btn.setToolTip('')

    def get_letter_value(self, let):
        cur = self.let_con.cursor()
        point = cur.execute(f'''SELECT value FROM letters WHERE char='{let}' ''')
        for j in point:
            return j[0]

    def update_grid(self, btns):
        for i, j in zip(self.grid, btns):
            for let, btn in zip(i, j):
                if let != '':
                    btn.stat = True
                    btn.setEnabled(False)
                btn.setText(let)

    def update_boosters(self, btns):
        for i, line in enumerate(btns):
            for j, btn in enumerate(line):
                btn.setProperty('boost', self.boosters.get((i, j), 0))

    def commit_grid(self, btns, chips):
        for i, line in enumerate(btns):
            for j, btn in enumerate(line):
                self.grid[i][j] = btn.text()
        for i, chip in enumerate(chips):
            self.curr_chips[i] = chip.text()

    def raise_chips(self, btns, cursor):
        for i in btns:
            if i.text() != '':
                self.chips.append(i.text())
                print(i.text())
        if cursor != '':
            self.chips.append(cursor)
            print(cursor)
        self.chips = random.sample(self.chips, len(self.chips))

    def input_word(self, btns, info, fist_word):
        res = ''
        intersect = False
        for i in range(info[2]):
            b = btns[get_x(info[0], i, info[3])][get_y(info[1], i, info[3])]
            if not fist_word and b.stat:
                intersect = True
            if fist_word and self.boosters.get((get_x(info[0], i, info[3]), get_y(info[1], i, info[3])), 0) == 5:
                intersect = True
            let = b.text()
            if let == '':
                self.log('Empty Space')
                return False
            res += let
        if res in self.words:
            self.log('Word already been!!!')
            return False
        self.words.append(res)
        if not intersect:
            self.log('Слово не пересекается с предыдущими.')
            return False
        return self.check_word(res)

    def word_points(self, info):
        res = 0
        cur = self.let_con.cursor()
        post_boost = []
        for i in range(info[2]):
            if info[3]:
                res += self.point_boost(info[0] + i, info[1], cur, post_boost)
            else:
                res += self.point_boost(info[0], info[1] + i, cur, post_boost)
        bonus = 0
        for i in post_boost:
            if i == 3:
                bonus += res
            if i == 4:
                bonus += res * 2
        print(f'Bonus: {bonus}')
        return res + bonus

    def point_boost(self, x, y, cur, post_boost):
        boost = self.boosters.get((x, y), 0)
        request = cur.execute(f'''SELECT value FROM letters WHERE char='{self.grid[x][y]}' ''')
        for j in request:
            res = j[0]
        print(f'Before boost: {res}')
        if boost == 0:
            print('x1')
            return res
        if boost == 1:
            print('x2')
            return res * 2
        if boost == 2:
            print('x3')
            return res * 3
        if boost == 3 or boost == 4:
            post_boost.append(boost)
        return res

    def close(self):
        self.let_con.close()

    # Problems with letter 'Е' and 'Ё'
    def check_word(self, word):
        res = self.morph.parse(word)
        for i in res:
            # print(i)
            if {'NOUN'} in i.tag and i.normal_form == word:
                return True
            else:
                print(f'Incorrect tags: {i}')
        print('--------------')
        return False

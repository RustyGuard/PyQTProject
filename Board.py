import sqlite3
import pymorphy2
import random


class Board:
    def __init__(self, log):
        self.let_con = sqlite3.connect('res/letters.db')
        self.morph = pymorphy2.MorphAnalyzer()
        self.words = []
        self.log = log
        # with open('res/word_rus.txt', mode='r', encoding='utf-8') as words:
        # self.words = map(lambda x: x.replace('\n', ''), words.readlines())

    def generate(self):
        self.grid = [[''] * 16 for _ in range(16)]
        self.chips = []
        cur = self.let_con.cursor()
        for i in cur.execute('''SELECT * FROM letters''').fetchall():
            for j in range(i[2]):
                self.chips.append(i[1])
        self.chips = random.sample(self.chips, len(self.chips))

    def take_chip(self):
        return self.chips.pop(-1)

    def next_chips(self):
        if len(self.chips) == 0:
            self.curr_chips = [''] * 7
        else:
            self.curr_chips = [self.take_chip() for _ in range(7)]

    def update_chips(self, btns):
        for i, btn in zip(self.curr_chips, btns):
            btn.setText(i)
            if i != '':
                btn.setToolTip(f'Очков за букву: {self.get_letter_points(i)}')
            else:
                btn.setToolTip('')

    def get_letter_points(self, let):
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

    def input_word(self, btns, info):
        res = ''
        for i in range(info[2]):
            if info[3]:
                let = btns[info[0] + i][info[1]].text()
            else:
                let = btns[info[0]][info[1] + i].text()
            if let == '':
                self.log('Empty Space')
                return False
            res += let
        if res in self.words:
            self.log('Word already been!!!')
            return False
        self.words.append(res)
        return self.check_word(res)

    def word_points(self, info):
        res = 0
        cur = self.let_con.cursor()
        for i in range(info[2]):
            if info[3]:
                let = self.grid[info[0] + i][info[1]]
            else:
                let = self.grid[info[0]][info[1] + i]
            point = cur.execute(f'''SELECT value FROM letters WHERE char='{let}' ''')
            for j in point:
                res += j[0]
        return res

    def close(self):
        self.let_con.close()

    def check_word(self, word):
        res = self.morph.parse(word)
        for i in res:
            # print(i)
            if {'NOUN', 'nomn'} in i.tag:
                # if i.score >= 0.5:
                print(f'PyMorphy foundt it: {i}')
                return True
                # else:
                # print(f'Low score: {i}')
            else:
                print(f'Incorrect tags: {i}')
        return False
        # return word in self.words

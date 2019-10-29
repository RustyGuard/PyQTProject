import sqlite3
# import pymorphy2
import random

class Board:
    def __init__(self):
        self.let_con = sqlite3.connect('res/letters.db')
        # self.morph = pymorphy2.MorphAnalyzer()
        with open('res/word_rus.txt', mode='r', encoding='utf-8') as words:
            self.words = map(lambda x: x.replace('\n', ''), words.readlines())

    def generate(self):
        self.grid = [[''] * 16 for _ in range(16)]
        self.chips = []
        cur = self.let_con.cursor()
        for i in cur.execute('''SELECT * FROM letters''').fetchall():
            # print(i)
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

    def update_grid(self, btns):
        for i, j in zip(self.grid, btns):
            for let, btn in zip(i, j):
                btn.setText(let)

    def close(self):
        self.let_con.close()

    # TODO Change word_rus.txt to pymorphy2
    def check_word(self, word):
        # res = self.morph.parse(word)
        return word in self.words

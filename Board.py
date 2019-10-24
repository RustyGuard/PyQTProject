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
            print(i)
            for j in range(i[2]):
                self.chips.append(i[1])
        self.chips = random.sample(self.chips, len(self.chips))

    def take_chip(self):
        return self.chips.pop(-1)

    def give_chip(self, btns):
        if len(self.chips) == 0:
            return -1
        for i in btns:
            i.setText(self.take_chip())
        return 0

    def close(self):
        self.let_con.close()

    # TODO Change word_rus.txt to pymorphy2
    def check_word(self, word):
        # res = self.morph.parse(word)
        return word in self.words

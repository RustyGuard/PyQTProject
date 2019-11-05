import sqlite3
import pymorphy2
import random
import socketserver


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


class BoardServer(socketserver.BaseRequestHandler):
    def __init__(self):
        self.let_con = sqlite3.connect('res/letters.db')
        self.morph = pymorphy2.MorphAnalyzer()
        self.words = []
        self.boosters = {}
        with open('res/boosters.txt') as f:
            for i, line in enumerate(f.readlines()):
                for j, boost in enumerate(line.split()):
                    if boost != 0:
                        self.boosters[j, i] = int(boost)

    def handle(self):
        socket = self.request[1]
        data = self.request[0].strip()
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        socket.sendto(data.upper(), self.client_address)


class Board:
    def __init__(self, log):
        self.let_con = sqlite3.connect('res/letters.db')
        self.morph = pymorphy2.MorphAnalyzer()
        self.words = []
        self.log = log
        self.boosters = {}
        with open('res/boosters.txt') as f:
            for i, line in enumerate(f.readlines()):
                for j, boost in enumerate(line.split()):
                    if boost != 0:
                        self.boosters[j, i] = int(boost)

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

    # 1 - x2 for letter
    # 2 - x3 for letter
    # 3 - x2 for word
    # 4 - x3 for word
    # 5 - Cell for first word
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

    def check_word(self, word):
        res = self.morph.parse(word)
        for i in res:
            # print(i)
            if {'NOUN'} in i.tag and i.normal_form.lower().replace('ё', 'е') == word:
                return True
            else:
                print(f'Incorrect tags: {i}')
        print('--------------')
        return False


if __name__ == '__main__':
    HOST, PORT = "192.168.0.221", 9999
    with socketserver.UDPServer((HOST, PORT), BoardServer) as server:
        server.serve_forever()

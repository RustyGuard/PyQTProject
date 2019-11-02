import sys

from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QPushButton, QApplication, QListWidgetItem, QMessageBox, QTableWidgetItem

from Board import Board
from ui_wordmaker import Ui_MainWindow
from game import Game


class WordMaker(Game, Ui_MainWindow):
    def __init__(self, parent, players=[['1st', QColor(0, 255, 0), 0]]):
        super().__init__(parent, 25)
        print('WordMaker!')
        self.grid = []
        self.players = players
        self.c_player = 0
        self.curr_oper = None
        self.curr_letter = ''
        self.add_player('2nd', 255, 0, 0)
        for i in range(16):
            line = []
            for j in range(16):
                b = QPushButton('', self)
                b.resize(35, 35)
                b.move(i * 36 + 10, j * 36)
                b.clicked.connect(self.chip_input)
                font = QFont()
                font.setFamily('Comic Sans MS')
                font.setPointSize(12)
                b.setFont(font)
                b.stat = False
                b.setProperty('selected', False)
                b.setProperty('grid', True)
                line.append(b)
            self.grid.append(line)

        self.buttons = [self.b0, self.b1, self.b2, self.b3, self.b4, self.b5, self.b6]
        for i in self.buttons:
            i.clicked.connect(self.chip_input)
            i.stat = False

        # Board
        self.board = Board(self.log)
        self.board.generate()
        self.board.next_chips()
        self.board.update_chips(self.buttons)
        self.board.update_boosters(self.grid)
        self.lock_grid()
        self.first_turn = True
        self.turn = 0

        # Events
        self.wordStart.clicked.connect(self.start_word)
        self.wordEnd.clicked.connect(self.end_word)
        self.turnEnd.clicked.connect(self.end_turn)
        self.turnCancel.clicked.connect(self.cancel_word)

        # Table
        self.tableWidget.setRowCount(len(self.players))
        self.tableWidget.setColumnCount(0)
        for i, pl in enumerate(self.players):
            item = QTableWidgetItem()
            item.setText(pl[0])
            self.tableWidget.setVerticalHeaderItem(i, item)
        with open('res/stylesheet.txt') as f:
            self.stylesheet = f.read()
        self.setStyleSheet(self.stylesheet)

    def log(self, msg):
        item = QListWidgetItem(msg)
        self.listWidget.addItem(item)

    def add_player(self, name, r=0, g=0, b=0):
        self.players.append([name, QColor(r, g, b), 0])
        print(self.players)

    def next_player(self):
        self.c_player = self.c_player + 1
        if self.c_player >= len(self.players):
            self.c_player = 0
            self.tableWidget.setColumnCount(self.turn + 1)
            for i, pl in enumerate(self.players):
                print(self.turn, i)
                self.tableWidget.setItem(i, self.turn, QTableWidgetItem(str(pl[2])))
            self.turn += 1
            if len(self.board.chips) < len(self.players) * 7:
                self.game_over()

    def game_over(self):
        self.lock_grid()
        self.lock_chips()
        self.wordStart.setEnabled(False)
        self.wordEnd.setEnabled(False)
        self.turnCancel.setEnabled(False)
        self.turnEnd.setEnabled(False)
        QMessageBox.about(self, 'Game over', 'В наборе закончились фишки.\nИгра завершена.')

    def get_curr_player(self):
        return self.players[self.c_player]

    def lock_grid(self):
        for i in self.grid:
            for j in i:
                j.setEnabled(False)

    def start_word(self):
        b = self.checkBox.isChecked()
        if (b and self.wordX.value() + self.wordLen.value() - 1 >= 16) or \
                (not b and self.wordY.value() + self.wordLen.value() - 1 >= 16):
            self.log('Out of bounds')
            return
        self.lock_grid()
        self.wordStart.setEnabled(False)
        self.wordEnd.setEnabled(True)
        self.turnCancel.setEnabled(True)
        self.turnEnd.setEnabled(False)
        self.curr_oper = (self.wordX.value(), self.wordY.value(), self.wordLen.value(), b)
        for i in range(self.wordLen.value()):
            if b:
                cell = self.grid[self.wordX.value() + i][self.wordY.value()]
            else:
                cell = self.grid[self.wordX.value()][self.wordY.value() + i]
            if not cell.stat:
                cell.setEnabled(True)

    def end_word(self):
        if self.board.input_word(self.grid, self.curr_oper, self.first_turn):
            self.board.commit_grid(self.grid, self.buttons)
            self.board.update_grid(self.grid)
            self.get_curr_player()[2] += self.board.word_points(self.curr_oper)
            self.log(f'У {self.get_curr_player()[0]} теперь {self.get_curr_player()[2]} очков!')
            self.lock_grid()
            self.wordStart.setEnabled(True)
            self.wordEnd.setEnabled(False)
            self.turnCancel.setEnabled(False)
            self.turnEnd.setEnabled(True)
            self.first_turn = False
        else:
            self.log('Invalid word!')

    def end_turn(self):
        old = self.get_curr_player()[0]
        self.next_player()
        self.board.raise_chips(self.buttons, self.curr_letter)
        self.board.next_chips()
        self.board.update_chips(self.buttons)
        self.lock_grid()
        self.curr_letter = ''
        self.cursorLet.setText('')
        self.log(f'Ход закончен для "{old}".')
        self.log(f'Следующий ход для "{self.get_curr_player()[0]}".')

    def unlock_cell(self, x, y):
        cell = self.grid[x][y]
        if not cell.stat:
            cell.setEnabled(True)

    def cancel_word(self):
        self.lock_grid()
        self.board.update_grid(self.grid)
        self.board.update_chips(self.buttons)
        self.curr_oper = None
        self.curr_letter = ''
        self.wordStart.setEnabled(True)
        self.wordEnd.setEnabled(False)
        self.turnCancel.setEnabled(False)
        self.turnEnd.setEnabled(True)

    def chip_input(self):
        btn = self.sender()
        a = btn.text()
        btn.setText(self.curr_letter)
        self.curr_letter = a
        if self.curr_letter != '':
            self.cursorLet.setText(f'Буква в руке: {self.curr_letter}')
        else:
            self.cursorLet.setText('')
        if btn.text() != '':
            btn.setToolTip(f'Очков за букву: {self.board.get_letter_value(btn.text())}')
        else:
            btn.setToolTip('')

    def lock_chips(self):
        self.set_chips_unlocked(False)

    def unlock_chips(self):
        self.set_chips_unlocked(True)

    def set_chips_unlocked(self, locked):
        for i in self.buttons:
            i.setEnabled(locked)

    def OnUpdate(self, delta):
        b = self.checkBox.isChecked()
        self.checkBox.setText('→' if b else '↓')
        for i in self.grid:
            for j in i:
                j.setProperty('selected', False)
        for i in range(self.wordLen.value()):
            if b:
                if self.wordX.value() + i < 16:
                    self.grid[self.wordX.value() + i][self.wordY.value()].setProperty('selected', True)
            else:
                if self.wordY.value() + i < 16:
                    self.grid[self.wordX.value()][self.wordY.value() + i].setProperty('selected', True)
        self.setStyleSheet(self.stylesheet)

    def closeEvent(self, e):
        self.board.close()
        Game.closeEvent(self, e)

    def getName(self):
        return 'WordMaker'


if __name__ == '__main__':
    a = QApplication(sys.argv)
    ex = WordMaker(None)
    ex.show()
    sys.exit(a.exec_())

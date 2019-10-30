import sys

from PyQt5.QtGui import QColor, QFont, QPalette, QPainter
from PyQt5.QtWidgets import QPushButton, QApplication, QListWidgetItem, QDialog, QMessageBox

from Board import Board
from ui_wordmaker import Ui_MainWindow
from game import Game


class WordMaker(Game, Ui_MainWindow):
    def __init__(self, parent, players=[['1st', QColor(0, 255, 0), 0]]):
        super().__init__(parent, 50)
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
                b.move(i * 36, j * 36)
                b.clicked.connect(self.chipInput)
                font = QFont()
                font.setFamily('Comic Sans MS')
                font.setPointSize(12)
                b.setFont(font)
                b.stat = False
                line.append(b)
            self.grid.append(line)

        self.buttons = [self.b0, self.b1, self.b2, self.b3, self.b4, self.b5, self.b6]
        for i in self.buttons:
            i.clicked.connect(self.chipInput)
            i.stat = False

        # Board
        self.board = Board(self.log)
        self.board.generate()
        self.board.next_chips()
        self.board.update_chips(self.buttons)
        self.lockGrid()
        # self.lockChips()

        # Events
        self.wordStart.clicked.connect(self.start_word)
        self.wordEnd.clicked.connect(self.end_word)
        self.turnEnd.clicked.connect(self.end_turn)
        self.turnCancel.clicked.connect(self.cancel_word)

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
            if len(self.board.chips) < len(self.players) * 7:
                self.game_over()

    def game_over(self):
        self.lockGrid()
        self.lockChips()
        self.wordStart.setEnabled(False)
        self.wordEnd.setEnabled(False)
        self.turnCancel.setEnabled(False)
        self.turnEnd.setEnabled(False)
        QMessageBox.about(self, 'Game over', 'В наборе закончились фишки.\nИгра завершена.')

    def getCurrPlayer(self):
        return self.players[self.c_player]

    def lockGrid(self):
        for i in self.grid:
            for j in i:
                j.setEnabled(False)

    def start_word(self):
        b = self.comboBox.currentText() == 'Горизонтально'
        if (b and self.wordX.value() + self.wordLen.value() - 1 >= 16) or \
                (not b and self.wordY.value() + self.wordLen.value() - 1 >= 16):
            self.log('Out of bounds')
            return
        self.lockGrid()
        self.wordStart.setEnabled(False)
        self.wordEnd.setEnabled(True)
        self.turnCancel.setEnabled(True)
        self.turnEnd.setEnabled(False)
        self.unlockChips()
        self.curr_oper = (self.wordX.value(), self.wordY.value(), self.wordLen.value(), b)
        for i in range(self.wordLen.value()):
            if b:
                self.unlockCell(self.wordX.value() + i, self.wordY.value())
            else:
                self.unlockCell(self.wordX.value(), self.wordY.value() + i)

    def end_word(self):
        if self.board.input_word(self.grid, self.curr_oper):
            self.board.commit_grid(self.grid, self.buttons)
            self.board.update_grid(self.grid)
            self.getCurrPlayer()[2] += self.board.word_points(self.curr_oper)
            self.log(f'У {self.getCurrPlayer()[0]} теперь {self.getCurrPlayer()[2]} очков!')
            self.lockGrid()
            self.wordStart.setEnabled(True)
            self.wordEnd.setEnabled(False)
            self.turnCancel.setEnabled(False)
            self.turnEnd.setEnabled(True)
        else:
            self.log('Invalid word!')

    def end_turn(self):
        old = self.getCurrPlayer()[0]
        # Skip
        self.next_player()
        self.board.raise_chips(self.buttons, self.curr_letter)
        self.board.next_chips()
        self.board.update_chips(self.buttons)
        self.lockGrid()
        self.curr_letter = ''
        self.cursorLet.setText('')
        # self.lockChips()
        self.log(f'Ход закончен для "{old}".')
        self.log(f'Следующий ход для "{self.getCurrPlayer()[0]}".')

    def unlockCell(self, x, y):
        cell = self.grid[x][y]
        if not cell.stat:
            cell.setEnabled(True)

    def cancel_word(self):
        # self.unlockChips()
        self.lockGrid()
        self.board.update_grid(self.grid)
        self.board.update_chips(self.buttons)
        self.curr_oper = None
        self.curr_letter = ''
        self.wordStart.setEnabled(True)
        self.wordEnd.setEnabled(False)
        self.turnCancel.setEnabled(False)
        self.turnEnd.setEnabled(True)

    def chipInput(self):
        btn = self.sender()
        a = btn.text()
        btn.setText(self.curr_letter)
        self.curr_letter = a
        if self.curr_letter != '':
            self.cursorLet.setText(f'Буква в руке: {self.curr_letter}')
        else:
            self.cursorLet.setText('')
        if btn.text() != '':
            btn.setToolTip(f'Очков за букву: {self.board.get_letter_points(btn.text())}')
        else:
            btn.setToolTip('')

    def lockChips(self):
        self.setChipsUnlocked(False)

    def unlockChips(self):
        self.setChipsUnlocked(True)

    # If button has .stat it can not be unlocked
    def setChipsUnlocked(self, locked):
        for i in self.buttons:
            if not i.stat:
                i.setEnabled(locked)

    def OnUpdate(self, delta):
        pass
        # print(delta)
        # self.board.give_chip(self.buttons)

    def closeEvent(self, e):
        self.board.close()
        Game.closeEvent(self, e)

    def getName(self):
        return 'WordMaker'

    def paintEvent(self, e):
        qp = QPainter(self)
        qp.setBrush(self.getCurrPlayer()[1])
        b = self.comboBox.currentText() == 'Горизонтально'
        if b:
            qp.drawRect(self.wordX.value() * 36 - 1, self.wordY.value() * 36 - 1, 36 * self.wordLen.value(), 36)
        else:
            qp.drawRect(self.wordX.value() * 36 - 1, self.wordY.value() * 36 - 1, 36, 36 * self.wordLen.value())


if __name__ == '__main__':
    a = QApplication(sys.argv)
    ex = WordMaker(None)
    ex.show()
    sys.exit(a.exec_())

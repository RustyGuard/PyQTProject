import sys

from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QPushButton, QApplication

from Board import Board
from ui_wordmaker import Ui_MainWindow
from game import Game


class WordMaker(Game, Ui_MainWindow):
    def __init__(self, parent, players=[('Me', QColor(0, 255, 0), 0)]):
        super().__init__(parent, 1000)
        print('WordMaker!')
        self.grid = []
        self.players = players
        self.c_player = 0
        self.curr_oper = None
        self.curr_letter = ''
        # self.add_player('Saske', 255, 0, 0)
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
        self.board = Board()
        self.board.generate()

        self.buttons = [self.b0, self.b1, self.b2, self.b3, self.b4, self.b5, self.b6]
        for i in self.buttons:
            i.clicked.connect(self.chipInput)
            i.stat = False
        self.board.next_chips()
        self.board.update_chips(self.buttons)
        self.lockGrid()
        self.lockChips()

        # Events
        self.wordStart.clicked.connect(self.start_word)
        self.wordEnd.clicked.connect(self.end_word)
        self.turnEnd.clicked.connect(self.end_turn)
        self.turnCancel.clicked.connect(self.cancel_turn)

    def add_player(self, name, r=0, g=0, b=0):
        self.players.append((name, QColor(r, g, b)))
        print(self.players)

    def next_player(self):
        self.c_player = (self.c_player + 1) % len(self.players)

    def getCurrPlayer(self):
        return self.players[self.c_player]

    def lockGrid(self):
        self.setGridUnlocked(False)

    def unlockGrid(self):
        self.setGridUnlocked(True)

    def start_word(self):
        self.lockGrid()
        self.wordStart.setEnabled(False)
        self.wordEnd.setEnabled(True)
        self.turnCancel.setEnabled(True)
        self.unlockChips()
        b = self.comboBox.currentText() == 'Горизонтально'
        if (b and self.wordX.value() + self.wordLen.value() - 1 >= 16) or \
                (not b and self.wordY.value() + self.wordLen.value() - 1 >= 16):
            print('Out of bounds')
            return
        self.curr_oper = (self.wordX.value(), self.wordY.value(), self.wordLen.value())
        for i in range(self.wordLen.value()):
            if b:
                self.grid[self.wordX.value() + i][self.wordY.value()].setEnabled(True)
            else:
                self.grid[self.wordX.value()][self.wordY.value() + i].setEnabled(True)

    def end_word(self):
        pass

    def end_turn(self):
        pass

    def cancel_turn(self):
        self.unlockChips()
        self.lockGrid()
        self.board.update_grid(self.grid)
        self.board.update_chips(self.buttons)
        self.curr_oper = None
        self.curr_letter = ''
        self.wordStart.setEnabled(True)
        self.wordEnd.setEnabled(False)
        self.turnCancel.setEnabled(False)

    def chipInput(self):
        btn = self.sender()
        a = btn.text()
        btn.setText(self.curr_letter)
        self.curr_letter = a

    def setGridUnlocked(self, locked):
        for i in self.grid:
            for j in i:
                j.setEnabled(locked)

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
        print(delta)
        # self.board.give_chip(self.buttons)

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

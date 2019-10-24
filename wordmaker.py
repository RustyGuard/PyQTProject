from Board import Board
from ui_wordmaker import Ui_MainWindow
from game import Game


class WordMaker(Game, Ui_MainWindow):
    def __init__(self, parent):
        super().__init__(parent, 1000)
        print('WordMaker!')
        self.board = Board()
        self.board.generate()
        self.buttons = [self.b0, self.b1, self.b2, self.b3, self.b4, self.b5, self.b6]
        self.board.give_chip(self.buttons)

    def OnUpdate(self, delta):
        print(delta)
        self.board.give_chip(self.buttons)

    def closeEvent(self, e):
        self.board.close()
        Game.closeEvent(self, e)

    def getName(self):
        return 'WordMaker'

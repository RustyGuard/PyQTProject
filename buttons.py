from ui_buttons import Ui_MainWindow
from game import Game


class Buttons(Game, Ui_MainWindow):
    def __init__(self, parent):
        super().__init__(parent, 1000)
        print('Btn!')

    def OnUpdate(self, delta):
        print(delta)


from PyQt5.QtWidgets import QMainWindow


class Game(QMainWindow):
    def __init__(self, parent, ups=None):
        super().__init__(parent)
        self.setupUi(self)
        if ups:
            self.updateTimer = self.startTimer(ups)
            self.delta = ups

    def OnUpdate(self, delta):
        pass

    def getName(self):
        return ''

    def timerEvent(self, e):
        self.OnUpdate(self.delta)
        self.update()

    def closeEvent(self, e):
        print('Window Closed')
        self.killTimer(self.updateTimer)
        e.accept()

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import sys
from ui_1 import Ui_MainWindow
from buttons import Buttons
from snake import SnakeWindow
from wordmaker import WordMaker


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.apps = {}
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)
        self.dialogs = list()

    def add_application(self, name, app):
        self.comboBox.addItem(name, app)

    def start(self):
        dialog = self.comboBox.currentData()(self)
        self.dialogs.append(dialog)
        dialog.show()


if __name__ == '__main__':
    a = QApplication(sys.argv)
    ex = MyWidget()
    ex.add_application('WordMaker', WordMaker)
    ex.add_application('Snake', SnakeWindow)
    ex.add_application('Buttons', Buttons)
    ex.show()
    sys.exit(a.exec_())

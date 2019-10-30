from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QLabel, QPushButton, QGroupBox
import sys
from ui_1 import Ui_MainWindow
# from buttons import Buttons
from snake import SnakeWindow
from wordmaker import WordMaker


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.apps = {}
        self.curr = -1
        self.setupUi(self)
        # self.pushButton.clicked.connect(self.start)
        self.dialogs = list()

    def add_application(self, name, app):
        self.curr += 1
        box = QGroupBox(self)
        box.move(self.curr * 150 + 25, 25)
        box.resize(145, 150)
        label = QLabel(name, box)
        label.resize(label.sizeHint())
        label.move(45, 25)
        btn = QPushButton('Старт', box)
        btn.app = app
        btn.resize(btn.sizeHint())
        btn.move(40, 75)
        btn.clicked.connect(self.start)
        # self.comboBox.addItem(name, app)

    def start(self):
        dialog = self.sender().app(self)
        self.dialogs.append(dialog)
        dialog.show()


if __name__ == '__main__':
    a = QApplication(sys.argv)
    ex = MyWidget()
    ex.add_application('WordMaker', WordMaker)
    ex.add_application('Snake', SnakeWindow)
    # Example
    # ex.add_application('Buttons', Buttons)
    ex.show()
    sys.exit(a.exec_())

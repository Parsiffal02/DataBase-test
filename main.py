import sys
from PyQt5 import QtWidgets
from application import MainWindow


def start():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    start()
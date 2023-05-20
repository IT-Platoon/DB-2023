import sys

from PyQt5 import QtWidgets

from swan_detector.windows import MainWindow


if __name__ == "__main__":
    application = QtWidgets.QApplication(sys.argv)
    application_window = MainWindow()
    application_window.show()
    application_window.setWindowTitle("Определение вида лебедя")
    application.exec_()

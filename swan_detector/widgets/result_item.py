from PyQt5 import QtWidgets, QtGui, QtCore
from pyqt_slideshow import SlideShow

from swan_detector.forms import Ui_ResultItem


class ResultItem(QtWidgets.QWidget):
    def __init__(self, image_paths: list, info: str) -> None:
        self.ui = Ui_ResultItem()
        self.ui.setupUi(self)
        self.image_paths = image_paths
        slider = SlideShow()
        slider.setFilenames(image_paths)
        slider.setTimerEnabled(False)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.insertWidget(0, slider)
        self.vbox.addStretch()
        self.widget.setLayout(self.vbox)
        slider.show()
        self.ui.info.setText(info)

    @QtCore.pyqtSlot()
    def on_left_button_clicked(self) -> None:
        pass

    @QtCore.pyqtSlot()
    def on_right_button_clicked(self) -> None:
        pass
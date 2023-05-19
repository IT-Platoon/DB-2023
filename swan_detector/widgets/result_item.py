from PyQt5 import QtWidgets, QtGui

from ..forms import Ui_ResultItem


class ResultItem(QtWidgets.QWidget, Ui_ResultItem):
    def __init__(self, image_path, info):
        self.setupUi(self)
        image = QtGui.QImage(image_path)
        pixmap = QtGui.QPixmap.fromImage(image)

        self.info.setText(info)
        self.image.setPixmap(pixmap)
        self.image.setScaledContents(True)

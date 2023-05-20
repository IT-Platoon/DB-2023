from PyQt5 import QtWidgets, QtCore

from swan_detector.forms import Ui_ResultDialog
from swan_detector.widgets import ResultItem


class ResultDialog(QtWidgets.QDialog):
    saveClicked = QtCore.pyqtSignal(str, bool)

    def __init__(self, info: dict):
        super().__init__()
        self.ui = Ui_ResultDialog()
        self.ui.setupUi(self)
        self.widget = QtWidgets.QWidget()
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.setSpacing(10)
        for image, swan in info.items():
            item = ResultItem(image, swan)
            self.vbox.insertWidget(0, item)
            self.vbox.addStretch()
        self.widget.setLayout(self.vbox)
        self.ui.list_detections.setWidget(self.widget)

    @QtCore.pyqtSlot()
    def on_ok_button_clicked(self) -> None:
        self.close()

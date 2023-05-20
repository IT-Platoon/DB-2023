from PyQt5 import QtWidgets, QtCore

from swan_detector.forms import Ui_ResultDialog
from swan_detector.widgets import ResultItem
from swan_detector.palettes import result_dialog_styles


class ResultDialog(QtWidgets.QDialog):
    saveClicked = QtCore.pyqtSignal(str, bool)

    def __init__(self, info: dict):
        super().__init__()
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.ui = Ui_ResultDialog()
        self.ui.setupUi(self)
        self.setMinimumSize(1120, 600)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.setSpacing(10)
        for item in info:
            images = [item["filename"], item["result_path"]]
            item = ResultItem(images, item["classes"])
            self.vbox.insertWidget(0, item)
            self.vbox.addStretch()
        self.ui.list_detections.setLayout(self.vbox)
        self.setStyleSheet(result_dialog_styles)

    @QtCore.pyqtSlot()
    def on_ok_button_clicked(self) -> None:
        self.close()

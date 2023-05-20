import os

from PyQt5 import QtCore, QtWidgets

from swan_detector.constants import (
    REFERENCE,
    RESULT_MESSAGE,
    MethodsLoad,
    SUCCESS_SELECT,
    FAILED_SELECT,
)
from swan_detector.forms import Ui_DetectionWindow
from swan_detector.model import load_model
from swan_detector.multithreading import Worker
from swan_detector.palettes import main_window_styles
from .result_dialog import ResultDialog


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DetectionWindow()
        self.ui.setupUi(self)
        self.directory_to_save = ""
        self.images = []
        self.ui.reference.setPlainText(REFERENCE)
        self.ui.reference.setReadOnly(True)
        self.setStyleSheet(main_window_styles)
        self.path_to_model = "swan_detector/model/weights/model.pt"
        self.model = None

    @QtCore.pyqtSlot()
    def on_load_button_clicked(self) -> None:
        right_extensions = (".jpeg", ".jpg", ".png")
        method_load = self.ui.comboBox.currentText()
        if MethodsLoad.GET_FILES == method_load:
            self.images, _ = QtWidgets.QFileDialog.getOpenFileNames(
                self,
                "Выберите картинки",
                "/",
                "Images (*.jpeg *.jpg *.png)",
            )
        elif MethodsLoad.GET_DIRECTORY == method_load:
            try:
                directory_to_load = QtWidgets.QFileDialog.getExistingDirectory(
                    self,
                    "Выберите директорию для загрузки картинок",
                    "/",
                )
                files = os.listdir(directory_to_load)
                self.images = [
                    os.path.join(directory_to_load, file)
                    for file in files
                    if file.endswith(right_extensions)
                ]
            except FileNotFoundError:
                pass
        self.directory_to_save = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Выберите директорию для загрузки конечного csv",
            "/",
        )
        if self.images and self.directory_to_save:
            if self.model is None:
                self.model = load_model(self.path_to_model)
            self.worker = Worker(
                self.images,
                self.directory_to_save,
                self.model,
            )
            self.worker.signals.finished.connect(self.finish_detecting)
            self.threadpool = QtCore.QThreadPool()
            self.threadpool.start(self.worker)
            QtWidgets.QMessageBox.warning(
                self,
                "Отлично!",
                SUCCESS_SELECT,
            )
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Ошибка!",
                FAILED_SELECT,
            )

    def finish_detecting(self, info: list) -> None:
        QtWidgets.QMessageBox.warning(
            self,
            "Детекция завершена!",
            RESULT_MESSAGE.format(directory_to_save=self.directory_to_save),
        )

        self.view_result = ResultDialog(info)
        self.view_result.show()
        self.view_result.exec_()

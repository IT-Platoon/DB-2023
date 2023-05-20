from PyQt5 import QtCore, QtWidgets

from swan_detector.constants import REFERENCE, RESULT_MESSAGE
from swan_detector.forms import Ui_DetectionWindow
from swan_detector.multithreading import Worker
from swan_detector.palettes import general_styles
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
        self.setStyleSheet(general_styles)

    @QtCore.pyqtSlot()
    def on_load_button_clicked(self) -> None:
        self.images, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            "Выберите картинки",
            "/",
            "Images (*.jpeg, *.jpg, *.png)",
        )
        self.directory_to_save = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Выберите директорию для загрузки картинки",
            "/",
        )
        if self.images and self.directory_to_save:
            self.worker = Worker(
                self.images,
                self.directory_to_save,
            )
            self.worker.signals.result.connect()
            self.worker.signals.finished.connect(self.finish_detecting)
            self.threadpool = QtCore.QThreadPool()
            self.threadpool.start(self.worker)
            QtWidgets.QMessageBox.warning(
                self,
                "Отлично!",
                "Файлы загружены. Процесс детекции начался.",
            )
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Ошибка!",
                "Выберите файлы для детекции и путь для выгрузки отчета.",
            )
    
    def finish_detecting(self, info: dict) -> None:
        QtWidgets.QMessageBox.warning(
            self,
            "Детекция завершена!",
            RESULT_MESSAGE.format(directory_to_save=self.directory_to_save),
        )

        self.choose_file_window = ResultDialog(info)
        self.choose_file_window.show()
        self.choose_file_window.exec_()

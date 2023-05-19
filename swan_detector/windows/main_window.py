from PyQt5 import QtCore, QtWidgets

from ..constants import REFERENCE
from ..forms import Ui_DetectionWindow
from ..multithreading import Worker
from ..palettes import general_styles


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
        print(self.images)
        print(self.directory_to_save)
        # добавить потоки...
        if self.images:
            self.worker = Worker()
            self.worker.signals.result.connect()
            self.worker.signals.finished.connect(self.finish_detecting)
            self.threadpool = QtCore.QThreadPool()
            self.threadpool.start(self.worker)
            QtWidgets.QMessageBox.warning(
                self,
                "Отлично!",
                "Файлы загружены",
            )
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Ошибка!",
                "Выберите файлы для детекции",
            )
    
    def finish_detecting(self) -> None:
        pass

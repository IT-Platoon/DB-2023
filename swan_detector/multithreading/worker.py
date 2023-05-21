from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread

from swan_detector.model import run_detection


class Worker(QThread):
    finished = pyqtSignal(list)
    def __init__(self, images: list[str], directory_to_save: str, model):
        super().__init__()
        self.images = images
        self.directory_to_save = directory_to_save
        self.model = model

    @pyqtSlot()
    def run(self):
        result = run_detection(
            self.model,
            self.images,
            self.directory_to_save,
        )
        self.finished.emit(result)

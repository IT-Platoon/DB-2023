from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject

from swan_detector.model import run_detection


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class Worker(QRunnable):
    def __init__(self, images: list[str], directory_to_save: str):
        super().__init__()
        self.images = images
        self.directory_to_save = directory_to_save

    @pyqtSlot()
    def run(self):
        run_detection()

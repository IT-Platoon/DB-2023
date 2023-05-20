from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject

from swan_detector.model import run_detection


class WorkerSignals(QObject):
    finished = pyqtSignal(list)


class Worker(QRunnable):
    
    def __init__(self, images: list[str], directory_to_save: str, model):
        super().__init__()
        self.signals = WorkerSignals()
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
        self.signals.finished.emit(result)

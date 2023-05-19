from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class Worker(QRunnable):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        pass

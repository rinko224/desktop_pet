from PySide2.QtWidgets import QWidget, QLabel
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, Qt


loader = QUiLoader()
class SetWindow(QWidget):
    def __init__(self):
        super().__init__()

        ui_file = QFile("ui/views/set_window.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

from PySide2.QtWidgets import QWidget
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, Qt

loader = QUiLoader()
class PetWindow(QWidget):
    def __init__(self):
        super().__init__()

        ui_file = QFile("ui/views/pet_window.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.init_window()
        

    def init_window(self):
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)



        

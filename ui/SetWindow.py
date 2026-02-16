from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QFileDialog, QSlider
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtCore import QFile, Qt, Signal


loader = QUiLoader()
class SetWindow(QWidget):
    imageChanged = Signal(str)
    sizeChanged = Signal(int)
    def __init__(self):
        super().__init__()

        ui_file = QFile("ui/views/set_window.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.setWindowTitle("桌宠设置")
        self.setWindowIcon(QIcon("resource/display/ran.ico"))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)

        self.picture_choose = self.ui.findChild(QPushButton, "picture_choose")
        self.picture_choose.clicked.connect(self.choose_picture)

        self.size_slider = self.ui.findChild(QSlider, "picture_resize")
        self.size_slider.setMinimum(10)
        self.size_slider.setMaximum(500)
        self.size_slider.setValue(100)
        self.size_slider.valueChanged.connect(self.update_size)

    def update_size(self, value):
        self.sizeChanged.emit(value)

    def choose_picture(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "",
            "Images (*.png *.jpg);;All Files (*)" 
        )

        if file_path:
            print("[info] 选择的图片路径:", file_path)
            self.imageChanged.emit(file_path)


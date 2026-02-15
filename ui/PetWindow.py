from PySide2.QtWidgets import QWidget, QLabel
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QMenu
from ui.SetWindow import SetWindow
from PySide2.QtWidgets import QApplication



loader = QUiLoader()
class PetWindow(QWidget):
    def __init__(self):
        super().__init__()

        ui_file = QFile("ui/views/pet_window.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.setting_page = SetWindow()

        self.init_window()
        self.init_picture()
        
        

    def init_window(self):
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

    def init_picture(self):
        picture = self.ui.findChild(QLabel, "Petlabel")

        picture.setPixmap(QPixmap("resource/display/ran.png"))

        picture.setAlignment(Qt.AlignCenter)

    def open_settings(self):
        self.setting_page.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos_active = True
            self._drag_pos = event.globalPos() - self.pos()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        settings_action = menu.addAction("Settings")
        exit_action = menu.addAction("Exit")

        action = menu.exec_(event.globalPos())

        if action == exit_action:
            QApplication.quit()
        elif action == settings_action:
            self.open_settings()






        

from PySide2.QtWidgets import QDialog,QWidget, QLabel, QStackedWidget, QSizePolicy, QInputDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtCore import QFile, Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QMenu
from ui.SetWindow import SetWindow
from PySide2.QtWidgets import QApplication
from core.chat.ChatCore import ChatCore
from ui.ChatDialog import ChatDialog
from ui.BubbleWidget import BubbleWidget
from core.chat.ChatWorker import ChatWorker


loader = QUiLoader()
class PetWindow(QWidget):
    def __init__(self):
        super().__init__()

        ui_file = QFile("ui/views/pet_window.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.setting_page = SetWindow()
        self.Petlabel = self.ui.findChild(QLabel, "Petlabel")

        self.setting_page.imageChanged.connect(self.update_picture)
        self.setting_page.sizeChanged.connect(self.update_size)

        self.chat_core = ChatCore()

        self.picture = None

        self.bubble = None

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
        self.picture = QPixmap("resource/display/ran.png")
        self.Petlabel.setPixmap(self.picture)
        
        self.Petlabel.setAlignment(Qt.AlignCenter)

        self.bubble = BubbleWidget(self, self.chat_core)

        picture_pos = self.Petlabel.geometry()
        self.bubble.move(picture_pos.x() + picture_pos.width() // 2 - self.bubble.width() // 2, picture_pos.y() + picture_pos.height())


    def open_settings(self):
        self.setting_page.resize(300, 400)
        self.setting_page.show()
        self.setting_page.raise_()

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
        chat_action = menu.addAction("Chat")

        action = menu.exec_(event.globalPos())

        if action == exit_action:
            QApplication.quit()
        elif action == settings_action:
            self.open_settings()
        elif action == chat_action:
            self.open_chat()

    def open_chat(self):
        dialog = ChatDialog()
        if dialog.exec_() == QDialog.Accepted:
            message = dialog.text_edit.toPlainText()
            self.bubble.start_chat(message)

    def update_picture(self, file_path):
        picture = self.ui.findChild(QLabel, "Petlabel")
        picture.setPixmap(QPixmap(file_path))
        self.picture = QPixmap(file_path)

    def update_size(self, value):
        ratio = value / 100.0
        
        new_picture = self.picture.scaled(
            self.picture.size() * ratio,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.Petlabel.setPixmap(new_picture)
        self.Petlabel.adjustSize()
        self.setFixedSize(new_picture.size())

    






        

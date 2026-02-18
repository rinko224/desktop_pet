from PySide2.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PySide2.QtCore import Qt, QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon


Loader = QUiLoader()
class ChatDialog(QDialog):
    def __init__(self):
        super().__init__()

        ui_file = QFile("ui/views/chat_dialog.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = Loader.load(ui_file)
        ui_file.close()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)

        self.setWindowTitle("桌宠聊天")
        self.setWindowIcon(QIcon("resource/display/ran.ico"))

        self.cancel = self.ui.findChild(QPushButton, "cancel")
        self.cancel.clicked.connect(self.reject)

        self.ensure = self.ui.findChild(QPushButton, "ensure")
        self.ensure.clicked.connect(self.accept)

        self.text_edit = self.ui.findChild(QTextEdit, "text_edit")






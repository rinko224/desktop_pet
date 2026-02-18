from PySide2.QtWidgets import QWidget, QLabel
from core.chat.ChatWorker import ChatWorker
from PySide2.QtGui import QPainter, QBrush, QColor, QFontMetrics
from PySide2.QtCore import Qt
from core.chat.ChatCore import ChatCore



class BubbleWidget(QWidget):
    def __init__(self, parent=None, chat_core: ChatCore = None):
        super().__init__(parent)

        self.max_width = 280
        self.padding = 20

        self.bubble_label = QLabel("", self)
        self.bubble_label.setWordWrap(True)
        self.bubble_label.move(10, 10)

        self.chat_core = chat_core

        self.bubble_text = ""
        self.current_index = 0
        self.hide()

    def start_chat(self, message):
        self.worker = ChatWorker(self.chat_core, message)
        self.worker.next_text_chunk.connect(self.update_bubble_text)
        self.worker.start()


    def update_bubble_text(self, chunk):
        self.bubble_text += chunk
        self.bubble_label.setText(self.bubble_text)
        self.adjustBubbleSize()
        self.show()
    
    def adjustBubbleSize(self):
        fm = QFontMetrics(self.bubble_label.font())

        # 计算单行文本宽度
        text_width = fm.horizontalAdvance(self.bubble_text)

        if text_width < self.max_width:
            bubble_width = text_width + self.padding
        else:
            bubble_width = self.max_width

        self.bubble_label.setFixedWidth(bubble_width - 20)
        self.bubble_label.adjustSize()

        bubble_height = self.bubble_label.height() + 20

        self.resize(bubble_width, bubble_height)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 15, 15)
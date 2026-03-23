from PySide2.QtWidgets import QWidget, QLabel, QPushButton
from core.chat.ChatWorker import ChatWorker
from PySide2.QtGui import QPainter, QBrush, QColor, QFontMetrics, QPainterPath, QPen
from PySide2.QtCore import Qt, QPointF, QRectF
from core.chat.ChatCore import ChatCore


class BubbleWidget(QWidget):
    def __init__(self, chat_core: ChatCore = None):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.max_width = 280
        self.padding = 20

        self.bubble_label = QLabel("", self)
        self.bubble_label.setWordWrap(True)
        self.bubble_label.move(10, 10)

        # 关闭按钮
        self.close_btn = QPushButton("×", self)
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #999;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #333;
            }
        """)
        self.close_btn.clicked.connect(self.hide)
        self.close_btn.hide()

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
        self.close_btn.show()

    def adjustBubbleSize(self):
        fm = QFontMetrics(self.bubble_label.font())

        # 计算单行文本宽度
        text_width = fm.horizontalAdvance(self.bubble_text)

        if text_width < self.max_width:
            bubble_width = text_width + self.padding
        else:
            bubble_width = self.max_width

        # 确保宽度至少为正数
        label_width = max(bubble_width - 40, 50)
        self.bubble_label.setFixedWidth(label_width)
        self.bubble_label.adjustSize()

        bubble_height = max(self.bubble_label.height() + 20, 40)

        self.resize(bubble_width, bubble_height)

        # 调整关闭按钮位置
        self.close_btn.move(bubble_width - 30, 5)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.end()  # 先结束 painter

        # 使用 QPainterPath 绘制带尾巴的气泡
        path = QPainterPath()

        w = self.width()
        h = self.height()

        # 气泡主体（省略右边30像素的区域给尾巴）
        path.moveTo(15, 0)
        path.lineTo(w - 45, 0)
        path.quadTo(w - 30, 0, w - 30, 15)
        path.lineTo(w - 30, h - 15)
        path.quadTo(w - 30, h, w - 15, h)
        path.lineTo(15, h)
        path.quadTo(0, h, 0, h - 15)
        path.lineTo(0, 15)
        path.quadTo(0, 0, 15, 0)
        path.closeSubpath()

        # 绘制尾巴（右下角）
        path.moveTo(w - 30, h - 10)
        path.quadTo(w - 10, h, w + 10, h + 10)
        path.quadTo(w - 10, h - 5, w - 30, h - 10)

        # 绘制
        painter2 = QPainter(self)
        painter2.setRenderHint(QPainter.Antialiasing)
        painter2.setBrush(QBrush(QColor(255, 255, 255)))
        painter2.setPen(QPen(QColor(200, 200, 200), 1))
        painter2.drawPath(path)
        painter2.end()

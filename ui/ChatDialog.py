from PySide2.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QWidget,
    QSizePolicy, QFrame
)
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QColor, QPixmap, QPainter, QPainterPath, QIcon
from qfluentwidgets import (
    PrimaryPushButton, TextEdit, SmoothScrollArea,
    ToolButton, FluentIcon, CardWidget
)
from core.chat.ChatCore import ChatCore
from core.chat.ChatWorker import ChatWorker
from pathlib import Path

BUBBLE_MAX_WIDTH_RATIO = 0.7


class AvatarLabel(QLabel):
    """圆形头像标签"""
    def __init__(self, image_path, size=40):
        super().__init__()
        self.setFixedSize(size, size)
        self.size = size
        self.update_avatar(image_path)

    def update_avatar(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            pixmap = QPixmap(self.size, self.size)
            pixmap.fill(QColor("#cccccc"))

        pixmap = pixmap.scaled(
            self.size, self.size,
            Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
        )

        rounded_pixmap = QPixmap(self.size, self.size)
        rounded_pixmap.fill(Qt.transparent)

        painter = QPainter(rounded_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, self.size, self.size)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        self.setPixmap(rounded_pixmap)


class ChatBubble(QFrame):
    """聊天气泡（固定颜色，不受重绘影响）"""
    def __init__(self, text, is_user=False, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.setFrameStyle(QFrame.NoFrame)

        self.label = QLabel(text, self)
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label.setStyleSheet("background: transparent; border: none;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.addWidget(self.label)

        self.setMaximumWidth(400)

        bg = "#0078D4" if is_user else "#F3F3F3"
        fg = "white" if is_user else "#1A1A1A"
        self.setStyleSheet(f"""
            ChatBubble {{
                background-color: {bg};
                border-radius: 12px;
                border: none;
            }}
            QLabel {{
                color: {fg};
                font-size: 14px;
                background: transparent;
                border: none;
            }}
        """)

    def text(self):
        return self.label.text()

    def setText(self, text):
        self.label.setText(text)


class ChatDialog(QDialog):
    def __init__(self, chat_core: ChatCore = None):
        super().__init__()

        self.setWindowTitle("与桌宠聊天")
        self.setWindowIcon(QIcon("resource/display/ran.ico"))
        self.resize(600, 750)
        self.setStyleSheet("""
            QDialog {
                background-color: #FAFAFA;
            }
        """)

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== 聊天滚动区域 =====
        self.scroll_area = SmoothScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            SmoothScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background: #CCCCCC;
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #AAAAAA;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(12)
        self.chat_layout.setContentsMargins(15, 15, 15, 15)
        self.chat_layout.addStretch()

        self.scroll_area.setWidget(self.chat_container)
        main_layout.addWidget(self.scroll_area, 1)

        # ===== 底部输入卡片（微信风格） =====
        bottom_card = CardWidget()
        bottom_card.setBorderRadius(0)
        bottom_card.setStyleSheet("""
            CardWidget {
                background-color: #F7F7F7;
                border-top: 1px solid #E0E0E0;
            }
        """)

        bottom_layout = QVBoxLayout(bottom_card)
        bottom_layout.setContentsMargins(12, 10, 12, 12)
        bottom_layout.setSpacing(8)

        # --- 工具栏（图标按钮） ---
        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        # 占位图标：HEART 后续可替换为自定义表情图标资源
        self.btn_emoji = ToolButton(FluentIcon.HEART)
        self.btn_emoji.setToolTip("发送表情")
        self.btn_emoji.clicked.connect(self.on_emoji_clicked)

        self.btn_screenshot = ToolButton(FluentIcon.CLIPPING_TOOL)
        self.btn_screenshot.setToolTip("截图")
        self.btn_screenshot.clicked.connect(self.on_screenshot_clicked)

        self.btn_file = ToolButton(FluentIcon.FOLDER)
        self.btn_file.setToolTip("上传文件")
        self.btn_file.clicked.connect(self.on_file_clicked)

        # 占位按钮，后续可扩展
        self.btn_image = ToolButton(FluentIcon.PHOTO)
        self.btn_image.setToolTip("发送图片")
        self.btn_image.clicked.connect(self.on_image_clicked)

        toolbar.addWidget(self.btn_emoji)
        toolbar.addWidget(self.btn_screenshot)
        toolbar.addWidget(self.btn_file)
        toolbar.addWidget(self.btn_image)
        toolbar.addStretch()

        bottom_layout.addLayout(toolbar)

        # --- 输入框 + 发送按钮 ---
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.text_edit = TextEdit(self)
        self.text_edit.setPlaceholderText("输入消息...")
        self.text_edit.setFixedHeight(80)
        self.text_edit.installEventFilter(self)

        self.send_btn = PrimaryPushButton("发送", self)
        self.send_btn.setFixedSize(70, 80)
        self.send_btn.clicked.connect(self.send_message)

        input_layout.addWidget(self.text_edit)
        input_layout.addWidget(self.send_btn)
        bottom_layout.addLayout(input_layout)

        main_layout.addWidget(bottom_card, 0)

        # ===== 数据初始化 =====
        self.chat_core = chat_core or ChatCore()
        self.message_history = []
        self.emotion = "neutral"
        self.user_avatar_path = "resource/display/ran.png"
        self.pet_avatar_path = "resource/display/ran.png"
        self.ai_label = None

    # ===== 工具栏占位槽函数 =====
    def on_emoji_clicked(self):
        """表情按钮点击（占位）"""
        print("[ui] 表情选择器（待实现）")

    def on_screenshot_clicked(self):
        """截图按钮点击（占位）"""
        print("[ui] 截图功能（待实现）")

    def on_file_clicked(self):
        """文件上传按钮点击（占位）"""
        print("[ui] 文件上传（待实现）")

    def on_image_clicked(self):
        """图片发送按钮点击（占位）"""
        print("[ui] 图片发送（待实现）")

    def eventFilter(self, obj, event):
        if obj == self.text_edit and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Return and not event.modifiers() == Qt.ShiftModifier:
                self.send_message()
                return True
        return super().eventFilter(obj, event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        max_width = int(self.width() * BUBBLE_MAX_WIDTH_RATIO)
        for i in range(self.chat_layout.count()):
            item = self.chat_layout.itemAt(i)
            if item and item.widget():
                container = item.widget()
                layout = container.layout()
                if not layout:
                    continue
                for j in range(layout.count()):
                    child_item = layout.itemAt(j)
                    if child_item and child_item.widget():
                        child = child_item.widget()
                        if isinstance(child, ChatBubble):
                            child.setMaximumWidth(max_width)

    def send_message(self):
        message = self.text_edit.toPlainText().strip()
        if not message:
            return

        self.message_history.append({"role": "user", "content": message})
        self.text_edit.clear()
        self.add_message(message, is_user=True)
        self.send_btn.setEnabled(False)
        self.ai_label = self.add_message("", is_user=False)

        self.worker = ChatWorker(self.chat_core, self.message_history)
        self.worker.emotion.connect(self.on_emotion)
        self.worker.next_text_chunk.connect(self.append_ai_response)
        self.worker.finished.connect(self.on_chat_finished)
        self.worker.start()

    def add_message(self, text, is_user: bool) -> ChatBubble:
        """添加消息到聊天区域"""
        bubble = ChatBubble(text, is_user)
        bubble.setMaximumWidth(int(self.width() * BUBBLE_MAX_WIDTH_RATIO))

        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(5, 2, 5, 2)
        container_layout.setSpacing(10)

        avatar_path = self.user_avatar_path if is_user else self.pet_avatar_path
        avatar = AvatarLabel(avatar_path, size=40)

        if is_user:
            container_layout.addStretch()
            container_layout.addWidget(bubble)
            container_layout.addWidget(avatar, alignment=Qt.AlignTop)
        else:
            container_layout.addWidget(avatar, alignment=Qt.AlignTop)
            container_layout.addWidget(bubble)
            container_layout.addStretch()

        self.remove_spacer()
        self.chat_layout.addWidget(container)
        self.add_spacer()
        self.scroll_to_bottom()

        return bubble

    def append_ai_response(self, chunk):
        if self.ai_label:
            self.ai_label.setText(self.ai_label.text() + chunk)
            self.scroll_to_bottom()

    def on_chat_finished(self, full_response):
        self.message_history.append({"role": "assistant", "content": full_response})
        self.send_btn.setEnabled(True)

    def on_emotion(self, emotion):
        self.emotion = emotion
        emotion_images = {
            "anger": "resource/emoji/anger/anger.png",
            "joy": "resource/emoji/joy/joy.png",
            "sad": "resource/emoji/sad/sad.png",
            "fear": "resource/emoji/fear/fear.png",
            "surprise": "resource/emoji/surprise/surprise.png",
        }
        image_path = emotion_images.get(emotion)
        if image_path:
            self.emit_emotion_image(image_path)

    def emit_emotion_image(self, image_path):
        if not Path(image_path).exists():
            return
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return

        image_label = QLabel()
        image_label.setPixmap(pixmap)

        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(55, 5, 5, 5)
        container_layout.addWidget(image_label)
        container_layout.addStretch()

        self.remove_spacer()
        self.chat_layout.addWidget(container)
        self.add_spacer()
        self.scroll_to_bottom()

    def remove_spacer(self):
        for i in range(self.chat_layout.count()):
            item = self.chat_layout.itemAt(i)
            if item.spacerItem():
                self.chat_layout.removeItem(item)
                break

    def add_spacer(self):
        self.chat_layout.addStretch()

    def scroll_to_bottom(self):
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

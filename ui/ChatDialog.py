from PySide2.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel, QWidget, QScrollArea, QHBoxLayout, QSizePolicy
from PySide2.QtCore import Qt, QFile, QSize
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon, QColor, QPalette, QPixmap
from core.chat.ChatCore import ChatCore
from core.chat.ChatWorker import ChatWorker
import json


CHAT_QSS = """
QDialog {
    background-color: #f5f5f5;
}

QScrollArea {
    background-color: white;
    border: none;
}

QTextEdit {
    background-color: white;
    border: none;
    border-top: 1px solid #e0e0e0;
    padding: 10px;
    font-family: "Microsoft YaHei", sans-serif;
    font-size: 14px;
}

QPushButton {
    background-color: #07B53A;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 10px 20px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #06a132;
}

QPushButton:pressed {
    background-color: #05902b;
}

QPushButton:disabled {
    background-color: #cccccc;
    color: #888888;
}
"""


USER_BUBBLE = """
QLabel {
    background-color: #95EC69;
    border-radius: 15px;
    padding: 10px 14px;
    color: #000000;
    font-size: 14px;
    font-weight: bold;
}"""

AI_BUBBLE = """
QLabel {
    background-color: #FFFFFF;
    border: 1px solid #e0e0e0;
    border-radius: 15px;
    padding: 10px 14px;
    color: #333333;
    font-size: 14px;
    font-weight: bold;
}"""

# 气泡最大宽度占比（相对于对话框宽度）
BUBBLE_MAX_WIDTH_RATIO = 0.7


class ChatDialog(QDialog):
    def __init__(self, chat_core: ChatCore = None):
        super().__init__()

        self.setStyleSheet(CHAT_QSS)

        ui_file = QFile("ui/views/chat_dialog.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = Loader.load(ui_file)
        ui_file.close()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)

        self.setWindowTitle("与桌宠聊天")
        self.setWindowIcon(QIcon("resource/display/ran.ico"))
        self.resize(600, 600)

        self.chat_core = chat_core or ChatCore()

        self.message_history = [] 

        self.emotion = "neutral"  # 当前对话情感状态

        # 获取UI组件
        self.scroll_area = self.ui.findChild(QScrollArea, "scrollArea")
        self.text_edit = self.ui.findChild(QTextEdit, "text_edit")
        self.send_btn = self.ui.findChild(QPushButton, "send_btn")

        # 获取聊天布局
        self.chat_layout = self.ui.findChild(QVBoxLayout, "chat_layout")

        # 发送按钮事件
        self.send_btn.clicked.connect(self.send_message)

        # 输入框回车发送（Shift+回车换行）
        self.text_edit.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.text_edit and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Return and not event.modifiers() == Qt.ShiftModifier:
                self.send_message()
                return True
        return super().eventFilter(obj, event)

    def resizeEvent(self, event):
        """窗口大小改变时更新气泡最大宽度"""
        super().resizeEvent(event)
        self.update_bubble_max_width()
        # 强制重新布局并更新
        self.chat_layout.activate()
        self.update()

    def get_bubble_max_width(self):
        """根据窗口宽度计算气泡最大宽度"""
        return int(self.width() * BUBBLE_MAX_WIDTH_RATIO)

    def update_bubble_max_width(self):
        """更新所有气泡的最大宽度"""
        max_width = self.get_bubble_max_width()
        for i in range(self.chat_layout.count()):
            item = self.chat_layout.itemAt(i)
            if item and item.widget():
                container = item.widget()
                # 只更新 label 的最大宽度，让容器保持原有的 sizePolicy
                for j in range(container.layout().count()):
                    child = container.layout().itemAt(j)
                    if child and child.widget() and isinstance(child.widget(), QLabel):
                        child.widget().setMaximumWidth(max_width)

    def send_message(self):
        message = self.text_edit.toPlainText().strip()
        if not message:
            return
        
        self.message_history.append({"role": "user", "content": message})

        # 清空输入框
        self.text_edit.clear()

        # 添加用户消息（右侧）
        self.add_message(message, is_user=True)

        # 禁用发送按钮
        self.send_btn.setEnabled(False)

        # 创建AI回复标签（左侧）
        self.ai_label = self.add_message("", is_user=False)

        # 启动聊天worker
        self.worker = ChatWorker(self.chat_core, self.message_history)
        self.worker.emotion.connect(self.on_emotion)

        self.worker.next_text_chunk.connect(self.append_ai_response)
        self.worker.finished.connect(self.on_chat_finished)

        self.worker.start()

    def add_message(self, text, is_user: bool) -> QLabel:
        """添加消息到聊天区域"""
        label = QLabel(text)
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        label.setMaximumWidth(self.get_bubble_max_width())

        # 用户消息样式（右侧，绿色气泡）
        if is_user:
            label.setStyleSheet(USER_BUBBLE)
            label.setAlignment(Qt.AlignLeft)
        else:
            # AI消息样式（左侧，白色气泡）
            label.setStyleSheet(AI_BUBBLE)
            label.setAlignment(Qt.AlignLeft)

        # 用水平容器控制左右对齐
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        if is_user:
            # 用户消息：stretch 在左边，推到右边
            container_layout.addStretch()
            container_layout.addWidget(label)
            # 用户气泡可以扩展
            container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        else:
            # AI消息：stretch 在右边，保持左边对齐
            container_layout.addWidget(label)
            container_layout.addStretch()
            # AI气泡使用 Preferred，让它根据内容自适应
            container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # 移除底部 spacer，添加消息，再添加 spacer
        self.remove_spacer()
        self.chat_layout.addWidget(container)
        self.add_spacer()

        # 滚动到底部
        self.scroll_to_bottom()

        return label

    def append_ai_response(self, chunk):
        """流式添加AI回复"""
        current = self.ai_label.text()
        self.ai_label.setText(current + chunk)

        # 自动滚动
        self.scroll_to_bottom()

    def on_chat_finished(self, full_response):
        """聊天结束"""
        self.message_history.append({"role": "assistant", "content": full_response})
        self.response_onetime = ""
        self.send_btn.setEnabled(True)

    def on_emotion(self, emotion):
        """接收情感状态更新并发出对应表情图片"""
        self.emotion = emotion
        print(f"[info] 当前情感状态: {emotion}")

        if(emotion == "neutral"):
            return
        # 情感对应的表情图片路径（先写死）
        emotion_images = {
            "anger": "resource/emoji/anger.png",
            "joy": "resource/emoji/joy.png",
            "sad": "resource/emoji/sad.png",
            "fear": "resource/emoji/fear.png",
            "surprise": "resource/emoji/surprise.png",
        }

        image_path = emotion_images.get(emotion)
        if image_path:
            self.emit_emotion_image(image_path)

    def emit_emotion_image(self, image_path):
        """在聊天区域显示表情图片"""
        from pathlib import Path
        if not Path(image_path).exists():
            print(f"[warning] 表情图片不存在: {image_path}")
            return

        # 加载图片
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"[warning] 加载图片失败: {image_path}")
            return

        # 创建显示图片的标签
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(False)

        # 用水平容器控制左右对齐
        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # AI图片：左边对齐
        container_layout.addWidget(image_label)
        container_layout.addStretch()
        container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # 添加到聊天布局
        self.remove_spacer()
        self.chat_layout.addWidget(container)
        self.add_spacer()

        # 滚动到底部
        self.scroll_to_bottom()


    def remove_spacer(self):
        """移除底部 spacer"""
        for i in range(self.chat_layout.count()):
            item = self.chat_layout.itemAt(i)
            if item.spacerItem():
                self.chat_layout.removeItem(item)
                break

    def add_spacer(self):
        """添加底部 spacer"""
        self.chat_layout.addStretch()

    def scroll_to_bottom(self):
        """滚动到最底部"""
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )


Loader = QUiLoader()

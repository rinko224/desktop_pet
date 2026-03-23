from PySide2.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel, QWidget, QScrollArea, QHBoxLayout, QSizePolicy
from PySide2.QtCore import Qt, QFile, QSize
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon, QColor, QPalette
from core.chat.ChatCore import ChatCore
from core.chat.ChatWorker import ChatWorker


class ChatDialog(QDialog):
    def __init__(self, chat_core: ChatCore = None):
        super().__init__()

        ui_file = QFile("ui/views/chat_dialog.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = Loader.load(ui_file)
        ui_file.close()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)

        self.setWindowTitle("与桌宠聊天")
        self.setWindowIcon(QIcon("resource/display/ran.ico"))
        self.resize(400, 500)

        self.chat_core = chat_core or ChatCore()

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

    def send_message(self):
        message = self.text_edit.toPlainText().strip()
        if not message:
            return

        # 清空输入框
        self.text_edit.clear()

        # 添加用户消息（右侧）
        self.add_message(message, is_user=True)

        # 禁用发送按钮
        self.send_btn.setEnabled(False)

        # 创建AI回复标签（左侧）
        self.ai_label = self.add_message("", is_user=False)

        # 启动聊天worker
        self.worker = ChatWorker(self.chat_core, message)
        self.worker.next_text_chunk.connect(self.append_ai_response)
        self.worker.finished.connect(self.on_chat_finished)
        self.worker.start()

    def add_message(self, text, is_user: bool) -> QLabel:
        """添加消息到聊天区域"""
        label = QLabel(text)
        label.setWordWrap(True)
        label.setMaximumWidth(280)

        # 用户消息样式（右侧，绿色背景）
        if is_user:
            label.setStyleSheet("""
                QLabel {
                    background-color: #95EC69;
                    border-radius: 10px;
                    padding: 8px 12px;
                    color: #000;
                }
            """)
            label.setAlignment(Qt.AlignLeft)
        else:
            # AI消息样式（左侧，白色背景）
            label.setStyleSheet("""
                QLabel {
                    background-color: #FFFFFF;
                    border: 1px solid #E0E0E0;
                    border-radius: 10px;
                    padding: 8px 12px;
                    color: #000;
                }
            """)
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
        else:
            # AI消息：stretch 在右边，保持左边对齐
            container_layout.addWidget(label)
            container_layout.addStretch()

        # 设置容器的 size policy 确保拉伸
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

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

    def on_chat_finished(self):
        """聊天结束"""
        self.send_btn.setEnabled(True)

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

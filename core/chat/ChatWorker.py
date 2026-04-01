from PySide2.QtCore import QThread, Signal
from core.chat.ChatCore import ChatCore


class ChatWorker(QThread):
    next_text_chunk = Signal(str)
    finished = Signal(str)

    def __init__(self, Chatcore: ChatCore, message_history):
        super().__init__()
        self.chatcore = Chatcore
        self.message_history = message_history

    def run(self):
        full_response = ""
        for chunk in self.chatcore.get_response(self.message_history):
            full_response += chunk
            self.next_text_chunk.emit(chunk)
        self.finished.emit(full_response)
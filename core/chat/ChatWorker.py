from PySide2.QtCore import QThread, Signal
from core.chat.ChatCore import ChatCore


class ChatWorker(QThread):
    next_text_chunk = Signal(str)
    finished = Signal()

    def __init__(self, Chatcore: ChatCore, message):
        super().__init__()
        self.chatcore = Chatcore
        self.message = message
    
    def run(self):
        for chunk in self.chatcore.get_response(self.message):
            self.next_text_chunk.emit(chunk)
        self.finished.emit()
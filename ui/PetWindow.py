from PySide2.QtWidgets import QWidget, QLabel, QStackedWidget, QSizePolicy, QInputDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtCore import QFile, Qt, QThread, Signal
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QMenu
from ui.SetWindow import SetWindow
from PySide2.QtWidgets import QApplication
from core.chat.ChatCore import ChatCore
from ui.ChatDialog import ChatDialog
from core.LiveSD.Live import LiveSDManager
from core.util.picture_deal import pil_to_pixmap
from core.config import config
from pathlib import Path


loader = QUiLoader()
CACHE_PATH = Path("resource/display/cache.png")


class LoadImageThread(QThread):
    """后台线程加载图片，避免卡顿"""
    finished = Signal(object)  # 加载完成的信号，传递 pixmap
    error = Signal(str)  # 错误信号

    def __init__(self, live_sd_manager, costume_id=None, character_id=None):
        super().__init__()
        self.live_sd_manager = live_sd_manager
        self.costume_id = costume_id
        self.character_id = character_id

    def run(self):
        try:
            if self.costume_id:
                self.live_sd_manager.gen_live(self.costume_id)
            elif self.character_id:
                self.live_sd_manager.random_live(self.character_id)
            else:
                self.live_sd_manager.random_live()
            picture = pil_to_pixmap(self.live_sd_manager.livesd)
            self.finished.emit(picture)
        except Exception as e:
            self.error.emit(str(e))


class PetWindow(QWidget):
    def __init__(self):
        super().__init__()

        ui_file = QFile("ui/views/pet_window.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)

        self.setting_page = SetWindow()
        self.Petlabel: QLabel = self.ui.findChild(QLabel, "Petlabel")

        self.setting_page.imageChanged.connect(self.update_picture)
        self.setting_page.sizeChanged.connect(self.update_size)
        self.setting_page.modeChanged.connect(self.on_mode_changed)

        self.chat_core: ChatCore = ChatCore()
        self.live_sd_manager: LiveSDManager = LiveSDManager()

        self.character_id: int = config.user_config["character_id"]
        self.current_costume_id: int = config.user_config["costume"]
        self.picture: QPixmap = None
        self._is_loading: bool = False  # 图片加载标志位

        self.init_window()
        self.init_picture()

        # 退出时保存缓存
        QApplication.instance().aboutToQuit.connect(self.save_cache)
        
        

    def init_window(self):
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

    def init_picture(self):
        # 优先从缓存加载
        if CACHE_PATH.exists():
            self.picture = QPixmap(str(CACHE_PATH))
            print("[info] 从缓存加载图片")
            self.Petlabel.setPixmap(self.picture)
            self.Petlabel.setAlignment(Qt.AlignCenter)
        else:
            # 没有缓存则下载，使用后台线程
            self._start_load_image(
                costume_id=self.current_costume_id if self.current_costume_id else None,
                character_id=self.character_id if not self.current_costume_id else None
            )

    def _on_image_loaded(self, picture):
        """图片加载完成回调"""
        self._is_loading = False
        self.picture = picture
        self.Petlabel.setPixmap(self.picture)
        self.Petlabel.setAlignment(Qt.AlignCenter)
        # 更新 costume_id 和 character_id（从 LiveSDManager 获取）
        self.current_costume_id = self.live_sd_manager.costume_id
        self.character_id = self.live_sd_manager.character_id
        # 保存到缓存
        self._save_to_cache()
        self._save_user_config()
        print("[info] 图片加载完成")

    def _on_image_error(self, error_msg):
        """图片加载失败回调"""
        self._is_loading = False
        print(f"[error] 图片加载失败: {error_msg}")

    def _start_load_image(self, costume_id=None, character_id=None):
        """开始加载图片（后台线程）"""
        if self._is_loading:
            print("[info] 图片正在加载中，跳过")
            return
        self._is_loading = True
        self._load_image_thread = LoadImageThread(
            self.live_sd_manager,
            costume_id=costume_id,
            character_id=character_id
        )
        self._load_image_thread.finished.connect(self._on_image_loaded)
        self._load_image_thread.error.connect(self._on_image_error)
        self._load_image_thread.start()

    def _save_to_cache(self):
        if self.live_sd_manager.livesd:
            self.live_sd_manager.livesd.save(str(CACHE_PATH))
            print("[info] 已保存缓存图片")

    def save_cache(self):
        self._save_to_cache()
        self._save_user_config()

    def _save_user_config(self):
        config.user_config["character_id"] = self.character_id
        config.user_config["costume"] = self.current_costume_id
        with open("resource/config/user.json", "w", encoding="utf-8") as f:
            import json
            json.dump(config.user_config, f, ensure_ascii=False, indent=4)
        print("[info] 已保存用户配置")


    def open_settings(self):
        self.setting_page.resize(500, 600)
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
        self.chat_dialog = ChatDialog(self.chat_core)
        self.chat_dialog.show()

    def update_picture(self, costume_id):
        self.current_costume_id = costume_id
        # 使用后台线程加载图片
        self._start_load_image(costume_id=costume_id)

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

    def on_mode_changed(self, mode, character_id):
        self.character_id = character_id
        if mode == SetWindow.MODE_MANUAL:
            # 手动模式保持当前图片不变，等待用户选择
            pass
        elif mode == SetWindow.MODE_CHAR_RANDOM:
            # 指定角色随机衣服
            self._start_load_image(character_id=character_id)
        elif mode == SetWindow.MODE_ALL_RANDOM:
            # 全部随机
            self._start_load_image()






        

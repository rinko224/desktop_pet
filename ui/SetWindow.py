from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QFileDialog, QSlider, QComboBox, QRadioButton
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtCore import QFile, Qt, Signal
from bestdori_ext import Character


STYLE_QSS = """
QWidget {
    background-color: #f5f5f5;
    color: #333333;
    font-family: "Microsoft YaHei", sans-serif;
    font-size: 14px;
}

QGroupBox {
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    margin-top: 10px;
    padding: 10px;
    background-color: white;
}

QGroupBox::title {
    color: #07B53A;
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 5px;
    font-weight: bold;
}

QPushButton {
    background-color: #07B53A;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 10px 24px;
    font-weight: bold;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #06a132;
}

QPushButton:pressed {
    background-color: #05902b;
}

QComboBox {
    background-color: white;
    color: #333333;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 8px 12px;
    min-height: 32px;
}

QComboBox:hover {
    border-color: #07B53A;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #888888;
    margin-right: 8px;
}

QLabel {
    color: #666666;
    font-weight: bold;
}

QSlider::groove:horizontal {
    background: #e0e0e0;
    height: 6px;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #07B53A;
    width: 18px;
    height: 18px;
    margin: -6px 0;
    border-radius: 9px;
    border: 2px solid white;
}

QSlider::handle:horizontal:hover {
    background: #06a132;
}

QSlider::sub-page:horizontal {
    background: #07B53A;
    border-radius: 3px;
}

QRadioButton {
    color: #333333;
    spacing: 8px;
}

QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 2px solid #e0e0e0;
    background-color: white;
}

QRadioButton::indicator:checked {
    background-color: #07B53A;
    border: 2px solid #07B53A;
}

QRadioButton::indicator:checked:hover {
    background-color: #06a132;
    border: 2px solid #06a132;
}
"""


loader = QUiLoader()
class SetWindow(QWidget):
    imageChanged = Signal(int)
    sizeChanged = Signal(int)
    # modeChanged 信号: (mode, character_id)
    # mode: 0=手动选择, 1=指定角色随机衣服, 2=全部随机
    # character_id: 仅在 mode=1 时有效
    modeChanged = Signal(int, int)

    # 模式: 0=手动选择, 1=指定角色随机衣服, 2=全部随机
    MODE_MANUAL = 0
    MODE_CHAR_RANDOM = 1
    MODE_ALL_RANDOM = 2

    def __init__(self):
        super().__init__()

        self.setStyleSheet(STYLE_QSS)

        ui_file = QFile("ui/views/set_window.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.setWindowTitle("桌宠设置")
        self.setWindowIcon(QIcon("resource/display/ran.ico"))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)

        # self.picture_choose: QPushButton = self.ui.findChild(QPushButton, "picture_choose")
        # self.picture_choose.clicked.connect(self.choose_picture)

        self.character_id: int = 1

        self.size_slider: QSlider = self.ui.findChild(QSlider, "picture_resize")
        self.size_slider.setMinimum(10)
        self.size_slider.setMaximum(500)
        self.size_slider.setValue(100)
        self.size_slider.valueChanged.connect(self.update_size)

        self.character_choose: QComboBox = self.ui.findChild(QComboBox, "character")
        self.character_choose.setCurrentIndex(0)

        self.costume_choose: QComboBox = self.ui.findChild(QComboBox, "costume")
        self.costume_init()

        self.character_choose.currentIndexChanged.connect(self.update_character)

        self.confirm_costume: QPushButton = self.ui.findChild(QPushButton, "confirm_costume")
        self.confirm_costume.clicked.connect(self.confirm_costume_clicked)

        # 模式选择
        self.radio_manual: QRadioButton = self.ui.findChild(QRadioButton, "radio_manual")
        self.radio_char_random: QRadioButton = self.ui.findChild(QRadioButton, "radio_char_random")
        self.radio_all_random: QRadioButton = self.ui.findChild(QRadioButton, "radio_all_random")

        self.radio_manual.toggled.connect(lambda checked: self.on_mode_changed(self.MODE_MANUAL) if checked else None)
        self.radio_char_random.toggled.connect(lambda checked: self.on_mode_changed(self.MODE_CHAR_RANDOM) if checked else None)
        self.radio_all_random.toggled.connect(lambda checked: self.on_mode_changed(self.MODE_ALL_RANDOM) if checked else None)

        self.current_mode = self.MODE_MANUAL

    def update_size(self, value):
        self.sizeChanged.emit(value)

    def on_mode_changed(self, mode):
        self.current_mode = mode
        # 根据模式控制控件的启用/禁用
        if mode == self.MODE_MANUAL:
            self.character_choose.setEnabled(True)
            self.costume_choose.setEnabled(True)
            self.confirm_costume.setEnabled(True)
        elif mode == self.MODE_CHAR_RANDOM:
            self.character_choose.setEnabled(True)
            self.costume_choose.setEnabled(False)
            self.confirm_costume.setEnabled(True)
        elif mode == self.MODE_ALL_RANDOM:
            self.character_choose.setEnabled(False)
            self.costume_choose.setEnabled(False)
            self.confirm_costume.setEnabled(True)
        # 发送模式变化信号
        self.modeChanged.emit(mode, self.character_id)

    def update_character(self, index):
        self.character_id = index + 1
        self.costume_choose.blockSignals(True)
        self.costume_init()
        self.costume_choose.setCurrentIndex(0)
        self.costume_choose.blockSignals(False)

    def confirm_costume_clicked(self):
        # 发送模式变化信号
        self.modeChanged.emit(self.current_mode, self.character_id)
        # 如果是手动模式，还发送图片变化信号
        if self.current_mode == self.MODE_MANUAL:
            costume_id = int(self.costume_choose.currentText())
            self.imageChanged.emit(costume_id)

    def choose_picture(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "",
            "Images (*.png *.jpg);;All Files (*)" 
        )

        if file_path:
            print("[info] 选择的图片路径:", file_path)
            self.imageChanged.emit(file_path)

    def costume_init(self):
        self.costume_choose.blockSignals(True)
        self.costume_choose.clear()
        character : Character.Character = Character.Character(self.character_id)
        costume_list = character.get_costume_list()
        self.costume_choose.addItems(costume_list)
        self.costume_choose.setCurrentIndex(0)
        self.costume_choose.blockSignals(False)

from PySide2.QtWidgets import (
    QWidget, QFileDialog, QVBoxLayout, QHBoxLayout,
    QFormLayout, QScrollArea, QSizePolicy
)
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt, Signal
from qfluentwidgets import (
    PushButton, PrimaryPushButton, ComboBox,
    RadioButton, Slider, CardWidget,
    SubtitleLabel, StrongBodyLabel, BodyLabel,
    SmoothScrollArea
)
from bestdori_ext import Character


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

    # 角色列表（与 ui 文件中的顺序一致）
    CHARACTER_NAMES = [
        "户山香澄", "花园多惠", "牛込里美", "山吹沙绫", "市谷有咲",
        "美竹兰", "青叶摩卡", "上原绯玛丽", "宇田川巴", "羽泽鸫",
        "丸山彩", "冰川日菜", "白鹭千圣", "大和麻弥", "若宫伊芙",
        "湊友希那", "冰川纱夜", "今井莉莎", "宇田川亚子", "白金燐子",
        "弦卷心", "濑田薰", "北泽育美", "松原花音", "奥泽美咲",
        "仓田真白", "桐谷透子", "广町七深", "二叶筑紫", "八潮瑠唯",
        "和奏瑞依", "朝日六花", "佐藤益木", "鳰原令王那", "珠手知由",
        "高松灯", "千早爱音", "要乐奈", "长崎爽世", "椎名立希",
    ]

    def __init__(self):
        super().__init__()

        self.setWindowTitle("桌宠设置")
        self.setWindowIcon(QIcon("resource/display/ran.ico"))
        self.resize(520, 640)
        self.setStyleSheet("""
            SetWindow {
                background-color: #F5F5F5;
            }
        """)

        self.character_id: int = 1
        self.current_mode = self.MODE_MANUAL

        # 滚动区域
        scroll = SmoothScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            SmoothScrollArea {
                border: none;
                background-color: #F5F5F5;
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

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(18)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setAlignment(Qt.AlignTop)

        # 标题
        title = SubtitleLabel("桌宠设置")
        layout.addWidget(title)
        layout.addWidget(BodyLabel("在这里调整桌宠的形象与行为"))

        # ========== 快捷操作卡片 ==========
        card_ops = CardWidget()
        card_ops.setBorderRadius(10)
        ops_layout = QHBoxLayout(card_ops)
        ops_layout.setSpacing(12)
        ops_layout.setContentsMargins(16, 16, 16, 16)

        self.api_setting = PushButton("输入 Deepseek API")
        self.character_setting = PushButton("导入人设文件")
        ops_layout.addWidget(self.api_setting)
        ops_layout.addWidget(self.character_setting)
        layout.addWidget(card_ops)

        # ========== 模式选择卡片 ==========
        card_mode = CardWidget()
        card_mode.setBorderRadius(10)
        mode_main_layout = QVBoxLayout(card_mode)
        mode_main_layout.setSpacing(12)
        mode_main_layout.setContentsMargins(16, 16, 16, 16)

        mode_main_layout.addWidget(StrongBodyLabel("随机模式"))
        mode_main_layout.addWidget(BodyLabel("选择桌宠形象的切换方式"))

        mode_inner = QVBoxLayout()
        mode_inner.setSpacing(8)
        self.radio_manual = RadioButton("手动选择")
        self.radio_manual.setChecked(True)
        self.radio_char_random = RadioButton("指定角色随机衣服")
        self.radio_all_random = RadioButton("全部随机")
        mode_inner.addWidget(self.radio_manual)
        mode_inner.addWidget(self.radio_char_random)
        mode_inner.addWidget(self.radio_all_random)
        mode_main_layout.addLayout(mode_inner)

        self.radio_manual.toggled.connect(
            lambda checked: self.on_mode_changed(self.MODE_MANUAL) if checked else None
        )
        self.radio_char_random.toggled.connect(
            lambda checked: self.on_mode_changed(self.MODE_CHAR_RANDOM) if checked else None
        )
        self.radio_all_random.toggled.connect(
            lambda checked: self.on_mode_changed(self.MODE_ALL_RANDOM) if checked else None
        )
        layout.addWidget(card_mode)

        # ========== 角色与服装卡片 ==========
        card_char = CardWidget()
        card_char.setBorderRadius(10)
        char_layout = QVBoxLayout(card_char)
        char_layout.setSpacing(14)
        char_layout.setContentsMargins(16, 16, 16, 16)

        char_layout.addWidget(StrongBodyLabel("形象设置"))

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignLeft)
        form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        self.character_choose = ComboBox()
        self.character_choose.addItems(self.CHARACTER_NAMES)
        self.character_choose.setCurrentIndex(0)
        self.character_choose.currentIndexChanged.connect(self.update_character)

        self.costume_choose = ComboBox()
        self.costume_init()

        self.confirm_costume = PrimaryPushButton("确认修改")
        self.confirm_costume.setFixedWidth(120)
        self.confirm_costume.clicked.connect(self.confirm_costume_clicked)

        form.addRow("选择人物", self.character_choose)
        form.addRow("服装选择", self.costume_choose)
        form.addRow("", self.confirm_costume)
        char_layout.addLayout(form)
        layout.addWidget(card_char)

        # ========== 缩放卡片 ==========
        card_scale = CardWidget()
        card_scale.setBorderRadius(10)
        scale_layout = QVBoxLayout(card_scale)
        scale_layout.setSpacing(12)
        scale_layout.setContentsMargins(16, 16, 16, 16)

        scale_layout.addWidget(StrongBodyLabel("图片缩放"))

        self.size_slider = Slider(Qt.Horizontal)
        self.size_slider.setMinimum(10)
        self.size_slider.setMaximum(500)
        self.size_slider.setValue(100)
        self.size_slider.valueChanged.connect(self.update_size)
        scale_layout.addWidget(self.size_slider)

        self.scale_label = BodyLabel("当前缩放: 100%")
        self.scale_label.setAlignment(Qt.AlignCenter)
        scale_layout.addWidget(self.scale_label)

        layout.addWidget(card_scale)
        layout.addStretch()

        scroll.setWidget(container)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def update_size(self, value):
        self.scale_label.setText(f"当前缩放: {value}%")
        self.sizeChanged.emit(value)

    def on_mode_changed(self, mode):
        self.current_mode = mode
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
        self.modeChanged.emit(mode, self.character_id)

    def update_character(self, index):
        self.character_id = index + 1
        self.costume_choose.blockSignals(True)
        self.costume_init()
        self.costume_choose.setCurrentIndex(0)
        self.costume_choose.blockSignals(False)

    def confirm_costume_clicked(self):
        self.modeChanged.emit(self.current_mode, self.character_id)
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
        character: Character.Character = Character.Character(self.character_id)
        costume_list = character.get_costume_list()
        self.costume_choose.addItems(costume_list)
        self.costume_choose.setCurrentIndex(0)
        self.costume_choose.blockSignals(False)

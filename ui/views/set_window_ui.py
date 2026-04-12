# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'set_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(544, 448)
        self.verticalLayout_5 = QVBoxLayout(Form)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox_3 = QGroupBox(Form)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.api_setting = QPushButton(self.groupBox_3)
        self.api_setting.setObjectName(u"api_setting")

        self.verticalLayout_3.addWidget(self.api_setting)


        self.horizontalLayout.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.character_setting = QPushButton(self.groupBox_2)
        self.character_setting.setObjectName(u"character_setting")

        self.verticalLayout_2.addWidget(self.character_setting)


        self.horizontalLayout.addWidget(self.groupBox_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_mode = QVBoxLayout()
        self.verticalLayout_mode.setObjectName(u"verticalLayout_mode")
        self.radio_manual = QRadioButton(self.groupBox)
        self.radio_manual.setObjectName(u"radio_manual")
        self.radio_manual.setChecked(True)

        self.verticalLayout_mode.addWidget(self.radio_manual)

        self.radio_char_random = QRadioButton(self.groupBox)
        self.radio_char_random.setObjectName(u"radio_char_random")

        self.verticalLayout_mode.addWidget(self.radio_char_random)

        self.radio_all_random = QRadioButton(self.groupBox)
        self.radio_all_random.setObjectName(u"radio_all_random")

        self.verticalLayout_mode.addWidget(self.radio_all_random)


        self.verticalLayout.addLayout(self.verticalLayout_mode)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.character = QComboBox(self.groupBox)
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.addItem("")
        self.character.setObjectName(u"character")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.character)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.costume = QComboBox(self.groupBox)
        self.costume.setObjectName(u"costume")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.costume)

        self.confirm_costume = QPushButton(self.groupBox)
        self.confirm_costume.setObjectName(u"confirm_costume")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.confirm_costume)


        self.verticalLayout.addLayout(self.formLayout)

        self.picture_resize = QSlider(self.groupBox)
        self.picture_resize.setObjectName(u"picture_resize")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.picture_resize.sizePolicy().hasHeightForWidth())
        self.picture_resize.setSizePolicy(sizePolicy)
        self.picture_resize.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.picture_resize)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.verticalLayout.setStretch(0, 4)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 1)

        self.verticalLayout_4.addWidget(self.groupBox)

        self.verticalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.setStretch(1, 2)

        self.verticalLayout_5.addLayout(self.verticalLayout_4)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"\u804a\u5929\u8bbe\u7f6e", None))
        self.api_setting.setText(QCoreApplication.translate("Form", u"\u8f93\u5165Deepseek API", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u4eba\u8bbe\u8bbe\u7f6e", None))
        self.character_setting.setText(QCoreApplication.translate("Form", u"\u5bfc\u5165\u4eba\u8bbe\u6587\u4ef6", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u5f62\u8c61\u8bbe\u7f6e", None))
        self.radio_manual.setText(QCoreApplication.translate("Form", u"\u624b\u52a8\u9009\u62e9", None))
        self.radio_char_random.setText(QCoreApplication.translate("Form", u"\u6307\u5b9a\u89d2\u8272\u968f\u673a\u8863\u670d", None))
        self.radio_all_random.setText(QCoreApplication.translate("Form", u"\u5168\u90e8\u968f\u673a", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u9009\u62e9\u4eba\u7269", None))
        self.character.setItemText(0, QCoreApplication.translate("Form", u"\u6237\u5c71\u9999\u6f84", None))
        self.character.setItemText(1, QCoreApplication.translate("Form", u"\u82b1\u56ed\u591a\u60e0", None))
        self.character.setItemText(2, QCoreApplication.translate("Form", u"\u725b\u8fbc\u91cc\u7f8e", None))
        self.character.setItemText(3, QCoreApplication.translate("Form", u"\u5c71\u5439\u6c99\u7eeb", None))
        self.character.setItemText(4, QCoreApplication.translate("Form", u"\u5e02\u8c37\u6709\u54b2", None))
        self.character.setItemText(5, QCoreApplication.translate("Form", u"\u7f8e\u7af9\u5170", None))
        self.character.setItemText(6, QCoreApplication.translate("Form", u"\u9752\u53f6\u6469\u5361", None))
        self.character.setItemText(7, QCoreApplication.translate("Form", u"\u4e0a\u539f\u7eef\u739b\u4e3d", None))
        self.character.setItemText(8, QCoreApplication.translate("Form", u"\u5b87\u7530\u5ddd\u5df4", None))
        self.character.setItemText(9, QCoreApplication.translate("Form", u"\u7fbd\u6cfd\u9e2b", None))
        self.character.setItemText(10, QCoreApplication.translate("Form", u"\u4e38\u5c71\u5f69", None))
        self.character.setItemText(11, QCoreApplication.translate("Form", u"\u51b0\u5ddd\u65e5\u83dc", None))
        self.character.setItemText(12, QCoreApplication.translate("Form", u"\u767d\u9e6d\u5343\u5723", None))
        self.character.setItemText(13, QCoreApplication.translate("Form", u"\u5927\u548c\u9ebb\u5f25", None))
        self.character.setItemText(14, QCoreApplication.translate("Form", u"\u82e5\u5bab\u4f0a\u8299", None))
        self.character.setItemText(15, QCoreApplication.translate("Form", u"\u6e4a\u53cb\u5e0c\u90a3", None))
        self.character.setItemText(16, QCoreApplication.translate("Form", u"\u51b0\u5ddd\u7eb1\u591c", None))
        self.character.setItemText(17, QCoreApplication.translate("Form", u"\u4eca\u4e95\u8389\u838e", None))
        self.character.setItemText(18, QCoreApplication.translate("Form", u"\u5b87\u7530\u5ddd\u4e9a\u5b50", None))
        self.character.setItemText(19, QCoreApplication.translate("Form", u"\u767d\u91d1\u71d0\u5b50", None))
        self.character.setItemText(20, QCoreApplication.translate("Form", u"\u5f26\u5377\u5fc3", None))
        self.character.setItemText(21, QCoreApplication.translate("Form", u"\u6fd1\u7530\u85b0", None))
        self.character.setItemText(22, QCoreApplication.translate("Form", u"\u5317\u6cfd\u80b2\u7f8e", None))
        self.character.setItemText(23, QCoreApplication.translate("Form", u"\u677e\u539f\u82b1\u97f3", None))
        self.character.setItemText(24, QCoreApplication.translate("Form", u"\u5965\u6cfd\u7f8e\u54b2", None))
        self.character.setItemText(25, QCoreApplication.translate("Form", u"\u4ed3\u7530\u771f\u767d", None))
        self.character.setItemText(26, QCoreApplication.translate("Form", u"\u6850\u8c37\u900f\u5b50", None))
        self.character.setItemText(27, QCoreApplication.translate("Form", u"\u5e7f\u753a\u4e03\u6df1", None))
        self.character.setItemText(28, QCoreApplication.translate("Form", u"\u4e8c\u53f6\u7b51\u7d2b", None))
        self.character.setItemText(29, QCoreApplication.translate("Form", u"\u516b\u6f6e\u7460\u552f", None))
        self.character.setItemText(30, QCoreApplication.translate("Form", u"\u548c\u594f\u745e\u4f9d", None))
        self.character.setItemText(31, QCoreApplication.translate("Form", u"\u671d\u65e5\u516d\u82b1", None))
        self.character.setItemText(32, QCoreApplication.translate("Form", u"\u4f50\u85e4\u76ca\u6728", None))
        self.character.setItemText(33, QCoreApplication.translate("Form", u"\u9cf0\u539f\u4ee4\u738b\u90a3", None))
        self.character.setItemText(34, QCoreApplication.translate("Form", u"\u73e0\u624b\u77e5\u7531", None))
        self.character.setItemText(35, QCoreApplication.translate("Form", u"\u9ad8\u677e\u706f", None))
        self.character.setItemText(36, QCoreApplication.translate("Form", u"\u5343\u65e9\u7231\u97f3", None))
        self.character.setItemText(37, QCoreApplication.translate("Form", u"\u8981\u4e50\u5948", None))
        self.character.setItemText(38, QCoreApplication.translate("Form", u"\u957f\u5d0e\u723d\u4e16", None))
        self.character.setItemText(39, QCoreApplication.translate("Form", u"\u690e\u540d\u7acb\u5e0c", None))

        self.label_3.setText(QCoreApplication.translate("Form", u"\u670d\u88c5\u9009\u62e9", None))
        self.confirm_costume.setText(QCoreApplication.translate("Form", u"\u786e\u8ba4\u4fee\u6539", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u56fe\u7247\u7f29\u653e", None))
    # retranslateUi


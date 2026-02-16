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
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.picture_choose = QPushButton(self.groupBox)
        self.picture_choose.setObjectName(u"picture_choose")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.picture_choose.sizePolicy().hasHeightForWidth())
        self.picture_choose.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.picture_choose)

        self.picture_resize = QSlider(self.groupBox)
        self.picture_resize.setObjectName(u"picture_resize")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.picture_resize.sizePolicy().hasHeightForWidth())
        self.picture_resize.setSizePolicy(sizePolicy1)
        self.picture_resize.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.picture_resize)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.verticalLayout.setStretch(0, 6)
        self.verticalLayout.setStretch(1, 4)
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
        self.picture_choose.setText(QCoreApplication.translate("Form", u"\u9009\u62e9\u56fe\u7247", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u56fe\u7247\u7f29\u653e", None))
    # retranslateUi


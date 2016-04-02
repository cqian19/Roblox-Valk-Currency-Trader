# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainGui.ui'
#
# Created: Thu Mar 10 22:58:13 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(649, 420)
        MainWindow.setMinimumSize(QtCore.QSize(649, 420))
        MainWindow.setMaximumSize(QtCore.QSize(649, 420))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setWeight(50)
        font.setBold(False)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/bot_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setStyleSheet("QMainWindow{\n"
"    background-color:rgb(240, 240, 240);\n"
"}")
        MainWindow.setIconSize(QtCore.QSize(1, 1))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtGui.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 20, 641, 391))
        self.stackedWidget.setStyleSheet("#page_3,#page_4{\n"
"    background-color:rgb(240, 240, 240);\n"
"}")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName("page_3")
        self.formFrame = QtGui.QFrame(self.page_3)
        self.formFrame.setGeometry(QtCore.QRect(190, 130, 271, 75))
        self.formFrame.setObjectName("formFrame")
        self.gridLayout = QtGui.QGridLayout(self.formFrame)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.gridLayout.setContentsMargins(-1, 20, -1, 1)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.usernameField = QtGui.QLineEdit(self.formFrame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setWeight(75)
        font.setBold(True)
        self.usernameField.setFont(font)
        self.usernameField.setStyleSheet("QLineEdit {\n"
"    border: 2px solid gray;\n"
"    border-radius: 9px;\n"
"    padding: 0 8px;\n"
"}")
        self.usernameField.setObjectName("usernameField")
        self.gridLayout.addWidget(self.usernameField, 0, 1, 1, 1)
        self.passwordField = QtGui.QLineEdit(self.formFrame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setWeight(75)
        font.setBold(True)
        self.passwordField.setFont(font)
        self.passwordField.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.passwordField.setStyleSheet("QLineEdit {\n"
"    border: 2px solid gray;\n"
"    border-radius: 9px;\n"
"    padding: 0 8px;\n"
"}")
        self.passwordField.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordField.setObjectName("passwordField")
        self.gridLayout.addWidget(self.passwordField, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.formFrame)
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        font.setPointSize(10)
        font.setWeight(50)
        font.setBold(False)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtGui.QLabel(self.formFrame)
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        font.setPointSize(10)
        font.setWeight(50)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.loginButton = QtGui.QPushButton(self.page_3)
        self.loginButton.setEnabled(True)
        self.loginButton.setGeometry(QtCore.QRect(270, 230, 131, 31))
        self.loginButton.setAutoFillBackground(False)
        self.loginButton.setStyleSheet("QPushButton\n"
"{\n"
"  border-image:url(:/images/login.png);\n"
"  icon-size: 130px, 50px;\n"
"}\n"
"\n"
"QPushButton:hover, QPushButton:pressed\n"
"{\n"
"  border-image: url(:/images/login_down.png);\n"
"  border: 1px solid red;\n"
"}\n"
"")
        self.loginButton.setText("")
        self.loginButton.setIconSize(QtCore.QSize(130, 50))
        self.loginButton.setFlat(True)
        self.loginButton.setObjectName("loginButton")
        self.verticalLayoutWidget = QtGui.QWidget(self.page_3)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(1, 1, 651, 102))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtGui.QLabel(self.verticalLayoutWidget)
        self.title.setAutoFillBackground(False)
        self.title.setText("")
        self.title.setPixmap(QtGui.QPixmap(":/images/logo.png"))
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.verticalLayoutWidget_4 = QtGui.QWidget(self.page_3)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, 270, 651, 80))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.errorMessage = QtGui.QLabel(self.verticalLayoutWidget_4)
        self.errorMessage.setEnabled(True)
        self.errorMessage.hide()
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setWeight(50)
        font.setBold(False)
        self.errorMessage.setFont(font)
        self.errorMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.errorMessage.setWordWrap(True)
        self.errorMessage.setObjectName("errorMessage")
        self.verticalLayout_4.addWidget(self.errorMessage)
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName("page_4")
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.page_4)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 651, 102))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.logo_page2 = QtGui.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.logo_page2.setFont(font)
        self.logo_page2.setAutoFillBackground(False)
        self.logo_page2.setText("")
        self.logo_page2.setPixmap(QtGui.QPixmap(":/images/logo.png"))
        self.logo_page2.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_page2.setObjectName("logo_page2")
        self.verticalLayout_2.addWidget(self.logo_page2)
        self.startButton = QtGui.QPushButton(self.page_4)
        self.startButton.setEnabled(True)
        self.startButton.setGeometry(QtCore.QRect(277, 330, 93, 32))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startButton.sizePolicy().hasHeightForWidth())
        self.startButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(10)
        font.setWeight(50)
        font.setBold(False)
        self.startButton.setFont(font)
        self.startButton.setObjectName("startButton")
        self.tabWidget_2 = QtGui.QTabWidget(self.page_4)
        self.tabWidget_2.setGeometry(QtCore.QRect(10, 90, 641, 231))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setWeight(75)
        font.setBold(True)
        self.tabWidget_2.setFont(font)
        self.tabWidget_2.setAutoFillBackground(False)
        self.tabWidget_2.setStyleSheet("QTabWidget::pane\n"
"{\n"
"    border-top: 2px solid #1B1B1B;\n"
"}\n"
"\n"
"QTabWidget::tab-bar\n"
"{\n"
"    left: 5px;\n"
"    alignment: left;\n"
"    background: #3E3E3E;\n"
"}\n"
"\n"
"QTabBar::tab\n"
"{\n"
"    border: 2px solid #C4C4C3;\n"
"    border-bottom-color: #C2C7CB; /* same as the pane color */\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"    min-width: 8ex;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"     background-color: qlineargradient(spread:reflect, x1:0.607, y1:0.483, x2:0.965, y2:0.482955, stop:0 rgba(235, 235, 235, 255), stop:1 rgba(255, 255, 255, 255));\n"
"    border-color: rgb(76, 76, 76);\n"
"    border-bottom-color: #C2C7CB; /* same as pane color */\n"
"}\n"
"\n"
"")
        self.tabWidget_2.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget_2.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget_2.setIconSize(QtCore.QSize(20, 20))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tabWidget_2Page1 = QtGui.QWidget()
        self.tabWidget_2Page1.setObjectName("tabWidget_2Page1")
        self.OptionsTabWidget = QtGui.QTabWidget(self.tabWidget_2Page1)
        self.OptionsTabWidget.setGeometry(QtCore.QRect(10, 1, 611, 241))
        font = QtGui.QFont()
        font.setFamily("Gadugi")
        font.setPointSize(8)
        font.setWeight(75)
        font.setBold(True)
        self.OptionsTabWidget.setFont(font)
        self.OptionsTabWidget.setStyleSheet("QGroupBox{ \n"
"     border: 2px solid gray; \n"
"     border-radius: 13px; \n"
"     border-width: 3px;\n"
"     background-color: rgb(240, 240, 240);\n"
" } ")
        self.OptionsTabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.OptionsTabWidget.setDocumentMode(True)
        self.OptionsTabWidget.setObjectName("OptionsTabWidget")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.groupBox = QtGui.QGroupBox(self.tab_3)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 611, 168))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setWeight(75)
        font.setBold(True)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.formLayoutWidget = QtGui.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 281, 184))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setVerticalSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.label_4)
        self.tixAmountLabel = QtGui.QLabel(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tixAmountLabel.sizePolicy().hasHeightForWidth())
        self.tixAmountLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.tixAmountLabel.setFont(font)
        self.tixAmountLabel.setObjectName("tixAmountLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.tixAmountLabel)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tixAmount = QtGui.QSpinBox(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tixAmount.sizePolicy().hasHeightForWidth())
        self.tixAmount.setSizePolicy(sizePolicy)
        self.tixAmount.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.tixAmount.setFont(font)
        self.tixAmount.setMaximum(999999999)
        self.tixAmount.setSingleStep(100)
        self.tixAmount.setObjectName("tixAmount")
        self.verticalLayout_5.addWidget(self.tixAmount)
        self.formLayout.setLayout(1, QtGui.QFormLayout.FieldRole, self.verticalLayout_5)
        self.tixTradeAllLabel = QtGui.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.tixTradeAllLabel.setFont(font)
        self.tixTradeAllLabel.setObjectName("tixTradeAllLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.tixTradeAllLabel)
        self.tixTradeAll = QtGui.QCheckBox(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tixTradeAll.sizePolicy().hasHeightForWidth())
        self.tixTradeAll.setSizePolicy(sizePolicy)
        self.tixTradeAll.setText("")
        self.tixTradeAll.setObjectName("tixTradeAll")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.tixTradeAll)
        self.splitTradesLabel = QtGui.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.splitTradesLabel.setFont(font)
        self.splitTradesLabel.setObjectName("splitTradesLabel")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.splitTradesLabel)
        self.tixSplitTrades = QtGui.QCheckBox(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tixSplitTrades.sizePolicy().hasHeightForWidth())
        self.tixSplitTrades.setSizePolicy(sizePolicy)
        self.tixSplitTrades.setText("")
        self.tixSplitTrades.setObjectName("tixSplitTrades")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.tixSplitTrades)
        self.formLayoutWidget_2 = QtGui.QWidget(self.groupBox)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(320, 10, 281, 161))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setVerticalSpacing(10)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_5 = QtGui.QLabel(self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.SpanningRole, self.label_5)
        self.robuxAmountLabel = QtGui.QLabel(self.formLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.robuxAmountLabel.sizePolicy().hasHeightForWidth())
        self.robuxAmountLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.robuxAmountLabel.setFont(font)
        self.robuxAmountLabel.setObjectName("robuxAmountLabel")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.robuxAmountLabel)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.robuxAmount = QtGui.QSpinBox(self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.robuxAmount.setFont(font)
        self.robuxAmount.setMaximum(999999999)
        self.robuxAmount.setSingleStep(10)
        self.robuxAmount.setObjectName("robuxAmount")
        self.verticalLayout_6.addWidget(self.robuxAmount)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.FieldRole, self.verticalLayout_6)
        self.robuxTradeAllLabel = QtGui.QLabel(self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.robuxTradeAllLabel.setFont(font)
        self.robuxTradeAllLabel.setObjectName("robuxTradeAllLabel")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.robuxTradeAllLabel)
        self.robuxTradeAll = QtGui.QCheckBox(self.formLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.robuxTradeAll.sizePolicy().hasHeightForWidth())
        self.robuxTradeAll.setSizePolicy(sizePolicy)
        self.robuxTradeAll.setText("")
        self.robuxTradeAll.setObjectName("robuxTradeAll")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.robuxTradeAll)
        self.robuxSplitTradesLabel = QtGui.QLabel(self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.robuxSplitTradesLabel.setFont(font)
        self.robuxSplitTradesLabel.setObjectName("robuxSplitTradesLabel")
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.robuxSplitTradesLabel)
        self.robuxSplitTrades = QtGui.QCheckBox(self.formLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.robuxSplitTrades.sizePolicy().hasHeightForWidth())
        self.robuxSplitTrades.setSizePolicy(sizePolicy)
        self.robuxSplitTrades.setText("")
        self.robuxSplitTrades.setObjectName("robuxSplitTrades")
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.robuxSplitTrades)
        self.frame = QtGui.QFrame(self.groupBox)
        self.frame.setGeometry(QtCore.QRect(290, 10, 31, 151))
        self.frame.setFrameShape(QtGui.QFrame.VLine)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.OptionsTabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.groupBox_2 = QtGui.QGroupBox(self.tab_4)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 0, 611, 168))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setWeight(75)
        font.setBold(True)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setStyleSheet("")
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayoutWidget_3 = QtGui.QWidget(self.groupBox_2)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 281, 154))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_3 = QtGui.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setVerticalSpacing(10)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_9 = QtGui.QLabel(self.formLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.SpanningRole, self.label_9)
        self.EarlyCancelTixLabel = QtGui.QLabel(self.formLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.EarlyCancelTixLabel.setFont(font)
        self.EarlyCancelTixLabel.setObjectName("EarlyCancelTixLabel")
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.EarlyCancelTixLabel)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.tixEarlyCancel = QtGui.QCheckBox(self.formLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tixEarlyCancel.sizePolicy().hasHeightForWidth())
        self.tixEarlyCancel.setSizePolicy(sizePolicy)
        self.tixEarlyCancel.setText("")
        self.tixEarlyCancel.setObjectName("tixEarlyCancel")
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.FieldRole, self.tixEarlyCancel)
        self.tixTradeAll_2 = QtGui.QCheckBox(self.formLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tixTradeAll_2.sizePolicy().hasHeightForWidth())
        self.tixTradeAll_2.setSizePolicy(sizePolicy)
        self.tixTradeAll_2.setText("")
        self.tixTradeAll_2.setObjectName("tixTradeAll_2")
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.FieldRole, self.tixTradeAll_2)
        self.tixEarlyCancel_2 = QtGui.QCheckBox(self.formLayoutWidget_3)
        self.tixEarlyCancel_2.setText("")
        self.tixEarlyCancel_2.setObjectName("tixEarlyCancel_2")
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.tixEarlyCancel_2)
        self.tixThresholdRate = QtGui.QDoubleSpinBox(self.formLayoutWidget_3)
        self.tixThresholdRate.setDecimals(3)
        self.tixThresholdRate.setMaximum(50.0)
        self.tixThresholdRate.setSingleStep(0.001)
        self.tixThresholdRate.setProperty("value", 20.0)
        self.tixThresholdRate.setObjectName("tixThresholdRate")
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.tixThresholdRate)
        self.formLayoutWidget_4 = QtGui.QWidget(self.groupBox_2)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(320, 10, 282, 151))
        self.formLayoutWidget_4.setObjectName("formLayoutWidget_4")
        self.formLayout_4 = QtGui.QFormLayout(self.formLayoutWidget_4)
        self.formLayout_4.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.formLayout_4.setVerticalSpacing(10)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_11 = QtGui.QLabel(self.formLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.SpanningRole, self.label_11)
        self.EarlyCancelRobuxLabel = QtGui.QLabel(self.formLayoutWidget_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.EarlyCancelRobuxLabel.sizePolicy().hasHeightForWidth())
        self.EarlyCancelRobuxLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.EarlyCancelRobuxLabel.setFont(font)
        self.EarlyCancelRobuxLabel.setObjectName("EarlyCancelRobuxLabel")
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.EarlyCancelRobuxLabel)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.robuxEarlyCancel = QtGui.QCheckBox(self.formLayoutWidget_4)
        self.robuxEarlyCancel.setText("")
        self.robuxEarlyCancel.setObjectName("robuxEarlyCancel")
        self.verticalLayout_8.addWidget(self.robuxEarlyCancel)
        self.formLayout_4.setLayout(1, QtGui.QFormLayout.FieldRole, self.verticalLayout_8)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_6)
        self.robuxThresholdRate = QtGui.QDoubleSpinBox(self.formLayoutWidget_4)
        self.robuxThresholdRate.setDecimals(3)
        self.robuxThresholdRate.setMaximum(50.0)
        self.robuxThresholdRate.setSingleStep(0.001)
        self.robuxThresholdRate.setObjectName("robuxThresholdRate")
        self.formLayout_4.setWidget(2, QtGui.QFormLayout.FieldRole, self.robuxThresholdRate)
        self.frame_2 = QtGui.QFrame(self.groupBox_2)
        self.frame_2.setGeometry(QtCore.QRect(290, 10, 31, 151))
        self.frame_2.setFrameShape(QtGui.QFrame.VLine)
        self.frame_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_2.setObjectName("frame_2")
        self.OptionsTabWidget.addTab(self.tab_4, "")
        self.tabWidget_2.addTab(self.tabWidget_2Page1, "")
        self.tabWidget_2Page2 = QtGui.QWidget()
        self.tabWidget_2Page2.setObjectName("tabWidget_2Page2")
        self.currentTradeTable = QtGui.QListWidget(self.tabWidget_2Page2)
        self.currentTradeTable.setGeometry(QtCore.QRect(20, 70, 271, 61))
        font = QtGui.QFont()
        font.setFamily("Lucida Sans Unicode")
        font.setWeight(50)
        font.setBold(False)
        self.currentTradeTable.setFont(font)
        self.currentTradeTable.setStyleSheet("QListWidget{\n"
"    background-color: white;\n"
"    alternate-background-color: rgb(243, 243, 243)\n"
"}")
        self.currentTradeTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.currentTradeTable.setAlternatingRowColors(True)
        self.currentTradeTable.setModelColumn(0)
        self.currentTradeTable.setUniformItemSizes(True)
        self.currentTradeTable.setObjectName("currentTradeTable")
        self.pastTradesTable = QtGui.QListWidget(self.tabWidget_2Page2)
        self.pastTradesTable.setGeometry(QtCore.QRect(320, 40, 291, 141))
        self.pastTradesTable.setStyleSheet("QListWidget{\n"
"    background-color: white;\n"
"    alternate-background-color: rgb(243, 243, 243)\n"
"}")
        self.pastTradesTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.pastTradesTable.setAlternatingRowColors(True)
        self.pastTradesTable.setModelColumn(0)
        self.pastTradesTable.setObjectName("pastTradesTable")
        self.label_7 = QtGui.QLabel(self.tabWidget_2Page2)
        self.label_7.setGeometry(QtCore.QRect(90, 50, 131, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtGui.QLabel(self.tabWidget_2Page2)
        self.label_8.setGeometry(QtCore.QRect(410, 18, 109, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.tabWidget_2.addTab(self.tabWidget_2Page2, "")
        self.stackedWidget.addWidget(self.page_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget_2.setCurrentIndex(0)
        self.currentTradeTable.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Valk TC Bot", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Username", None, QtGui.QApplication.UnicodeUTF8))
        self.errorMessage.setText(QtGui.QApplication.translate("MainWindow", "<html><head/><body><p><span style=\" color:#000000;\">Login failed! Note that Roblox will lock you out after a certain number of failed attempts.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.startButton.setText(QtGui.QApplication.translate("MainWindow", "Trade", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Tix", None, QtGui.QApplication.UnicodeUTF8))
        self.tixAmountLabel.setText(QtGui.QApplication.translate("MainWindow", "Amount to trade:", None, QtGui.QApplication.UnicodeUTF8))
        self.tixTradeAllLabel.setText(QtGui.QApplication.translate("MainWindow", "Trade all:", None, QtGui.QApplication.UnicodeUTF8))
        self.splitTradesLabel.setText(QtGui.QApplication.translate("MainWindow", "Split trades", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Robux", None, QtGui.QApplication.UnicodeUTF8))
        self.robuxAmountLabel.setText(QtGui.QApplication.translate("MainWindow", "Amount to trade:", None, QtGui.QApplication.UnicodeUTF8))
        self.robuxTradeAllLabel.setText(QtGui.QApplication.translate("MainWindow", "Trade all:", None, QtGui.QApplication.UnicodeUTF8))
        self.robuxSplitTradesLabel.setText(QtGui.QApplication.translate("MainWindow", "Split trades", None, QtGui.QApplication.UnicodeUTF8))
        self.OptionsTabWidget.setTabText(self.OptionsTabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Basic", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Tix", None, QtGui.QApplication.UnicodeUTF8))
        self.EarlyCancelTixLabel.setText(QtGui.QApplication.translate("MainWindow", "Early Split Trade Cancel:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Trade when rate is below:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("MainWindow", "Robux", None, QtGui.QApplication.UnicodeUTF8))
        self.EarlyCancelRobuxLabel.setText(QtGui.QApplication.translate("MainWindow", "Early Split Trade Cancel:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Trade when rate is above:", None, QtGui.QApplication.UnicodeUTF8))
        self.OptionsTabWidget.setTabText(self.OptionsTabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("MainWindow", "Advanced", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabWidget_2Page1), QtGui.QApplication.translate("MainWindow", "Bot", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Current Trades", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Trade Log", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabWidget_2Page2), QtGui.QApplication.translate("MainWindow", "Trade Log", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc

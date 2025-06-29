# ruff: noqa
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QDoubleSpinBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QListView,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setViewMode(QListView.IconMode)
        self.listWidget.setIconSize(QSize(100, 100))
        self.listWidget.setResizeMode(QListView.Adjust)

        self.horizontalLayout.addWidget(self.listWidget)

        self.groupLayout = QVBoxLayout()
        self.groupLayout.setObjectName("groupLayout")
        self.groupListWidget = QListWidget(self.centralwidget)
        self.groupListWidget.setObjectName("groupListWidget")
        self.groupListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.groupLayout.addWidget(self.groupListWidget)

        self.addGroupButton = QPushButton(self.centralwidget)
        self.addGroupButton.setObjectName("addGroupButton")

        self.groupLayout.addWidget(self.addGroupButton)

        self.thresholdLayout = QHBoxLayout()
        self.thresholdLayout.setObjectName("thresholdLayout")
        self.thresholdLabel = QLabel(self.centralwidget)
        self.thresholdLabel.setObjectName("thresholdLabel")

        self.thresholdLayout.addWidget(self.thresholdLabel)

        self.thresholdSpinBox = QDoubleSpinBox(self.centralwidget)
        self.thresholdSpinBox.setObjectName("thresholdSpinBox")
        self.thresholdSpinBox.setDecimals(2)
        self.thresholdSpinBox.setMaximum(1.000000000000000)
        self.thresholdSpinBox.setSingleStep(0.050000000000000)
        self.thresholdSpinBox.setValue(0.300000000000000)

        self.thresholdLayout.addWidget(self.thresholdSpinBox)

        self.groupLayout.addLayout(self.thresholdLayout)

        self.assignButton = QPushButton(self.centralwidget)
        self.assignButton.setObjectName("assignButton")

        self.groupLayout.addWidget(self.assignButton)

        self.partitionButton = QPushButton(self.centralwidget)
        self.partitionButton.setObjectName("partitionButton")

        self.groupLayout.addWidget(self.partitionButton)

        self.resultTreeWidget = QTreeWidget(self.centralwidget)
        self.resultTreeWidget.setObjectName("resultTreeWidget")
        self.resultTreeWidget.setHeaderHidden(True)

        self.groupLayout.addWidget(self.resultTreeWidget)

        self.horizontalLayout.addLayout(self.groupLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 640, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Image Partitioner", None)
        )
        self.actionOpen.setText(
            QCoreApplication.translate("MainWindow", "&Open Folder...", None)
        )
        self.actionExit.setText(QCoreApplication.translate("MainWindow", "E&xit", None))
        self.addGroupButton.setText(
            QCoreApplication.translate("MainWindow", "Add Group", None)
        )
        self.thresholdLabel.setText(
            QCoreApplication.translate("MainWindow", "Threshold", None)
        )
        self.assignButton.setText(
            QCoreApplication.translate("MainWindow", "Assign Selected Images", None)
        )
        self.partitionButton.setText(
            QCoreApplication.translate("MainWindow", "Auto Partition", None)
        )
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "&File", None))

    # retranslateUi

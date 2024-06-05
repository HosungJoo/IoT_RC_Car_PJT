# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainUI.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide2.QtWidgets import (QApplication, QDial, QMainWindow, QMenuBar,
    QPlainTextEdit, QPushButton, QScrollBar, QSizePolicy,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 480)
        font = QFont()
        font.setFamilies([u"Sitka Display"])
        font.setPointSize(9)
        font.setBold(False)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.handle = QDial(self.centralwidget)
        self.handle.setObjectName(u"handle")
        self.handle.setGeometry(QRect(320, 240, 161, 171))
        self.vellocity_bar = QScrollBar(self.centralwidget)
        self.vellocity_bar.setObjectName(u"vellocity_bar")
        self.vellocity_bar.setGeometry(QRect(130, 220, 71, 191))
        self.vellocity_bar.setAcceptDrops(False)
        self.vellocity_bar.setMaximum(230)
        self.vellocity_bar.setOrientation(Qt.Orientation.Vertical)
        self.forward_btn = QPushButton(self.centralwidget)
        self.forward_btn.setObjectName(u"forward_btn")
        self.forward_btn.setGeometry(QRect(550, 230, 121, 51))
        self.backward_btn = QPushButton(self.centralwidget)
        self.backward_btn.setObjectName(u"backward_btn")
        self.backward_btn.setGeometry(QRect(550, 340, 121, 51))
        self.log_data = QPlainTextEdit(self.centralwidget)
        self.log_data.setObjectName(u"log_data")
        self.log_data.setGeometry(QRect(130, 10, 271, 181))
        self.sensing_data = QPlainTextEdit(self.centralwidget)
        self.sensing_data.setObjectName(u"sensing_data")
        self.sensing_data.setGeometry(QRect(410, 10, 271, 181))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 28))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.forward_btn.setText(QCoreApplication.translate("MainWindow", u"Forward", None))
        self.backward_btn.setText(QCoreApplication.translate("MainWindow", u"Backward", None))
    # retranslateUi


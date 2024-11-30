import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSlider, QPushButton, QWidget, QHBoxLayout, \
    QSizePolicy, QGridLayout, QAction, QMenuBar, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QMouseEvent

class MenuBar(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)

        self.init_menu()

    def init_menu(self):

        # Добавление разделов в меню-бар
        view_menu = self.addMenu("Внешний вид")
        setting_menu = self.addMenu("Настройки")
        about_menu = self.addMenu("Об авторе")

        about_action = QAction("About", self)

        about_menu.addAction(about_action)

    def show_about_dialog(self):
        pass

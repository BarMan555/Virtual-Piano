import sys
import json
import pygame.mixer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QKeyEvent, QIcon
from checkLicense import validate_license
from recorder import Recorder
from metronome import Metronome
from menuBar import MenuBar
from pianoControlPanel import PianoControlPanel
from pianoKeyboard import PianoKeyboard
from volume import VolumeControl
from loguru import logger

# Открываем файл и загружаем его содержимое
with open("hot_key.json", "r", encoding="utf-8") as file:
    hot_key = json.load(file)

# Инициализация микшера pygame
pygame.mixer.init()
pygame.mixer.set_num_channels(64)

# Добавляем логирование в файл
logger.add("debug/debug.log", format="{time} - {level} - {message}", level="DEBUG")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Проверяем лицензию
        if not validate_license():
            self.show_license_error()
            sys.exit(0)  # Завершаем приложение, если лицензия невалидна

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Virtual Piano")
        self.setWindowIcon((QIcon("icon/piano.ico")))
        self.setFixedSize(1200, 400)

        volume_control = VolumeControl()
        recorder = Recorder()
        metronome = Metronome(bpm=60)
        menu_bar = MenuBar(self)

        # Меню сверху
        self.setMenuBar(menu_bar)

        # Нижняя панель пианино
        self.piano_panel = PianoKeyboard(volume_control, recorder)

        # Верхняя панель управления
        control_panel = PianoControlPanel(volume_control, recorder, metronome, self.piano_panel)

        # Для отображения нажатых клавиш на панеле управления
        self.piano_panel.key_pressed.connect(control_panel.update_pressed_keys)

        # Основной макет
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 0, 0, 0)  # Отступы: слева, сверху, справа, снизу
        main_layout.setSpacing(0)
        main_layout.addWidget(control_panel)
        main_layout.addWidget(self.piano_panel)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_license_error(self):
        """Отображение окна с сообщением об ошибке лицензии."""
        error_msg = QMessageBox()
        error_msg.setIcon(QMessageBox.Critical)
        error_msg.setWindowTitle("Ошибка лицензии")
        error_msg.setText("Невозможно запустить приложение.\nЛицензионный ключ недействителен.")
        error_msg.setStandardButtons(QMessageBox.Ok)
        error_msg.exec_()

    def keyPressEvent(self, event: QKeyEvent):
        """Обработка нажатий клавиш."""

        # Чтобы не было многократного нажатия зажатой клавиши
        if event.isAutoRepeat():
            return

        key = hot_key.get(str(event.key()))
        if key is not None:
            self.piano_panel.keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """Обработка отпускания клавиш."""

        # Чтобы не было многократного нажатия зажатой клавиши
        if event.isAutoRepeat():
            return

        key = hot_key.get(str(event.key()))
        if key is not None:
            self.piano_panel.keyReleaseEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
 
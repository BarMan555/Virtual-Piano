import pygame.mixer
import json
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QMouseEvent, QKeyEvent
from loguru import logger
from pygame.examples.midi import null_key

# Открываем файл и загружаем его содержимое
with open("hot_key.json", "r", encoding="utf-8") as file:
    hot_key = json.load(file)

# Путь к папке со звуками
SOUND_PATH = "sounds/"



class PianoKeyboard(QWidget):
    key_pressed = pyqtSignal(set)

    def __init__(self, volume_control, recorder, key = null_key):
        super().__init__()
        self.setShortcutAutoRepeat(False)
        self.volume_control = volume_control
        self.recorder = recorder

        # Конфигурация клавиш
        self.num_white_keys = 36
        self.num_black_keys = self.num_white_keys // 7 * 5

        self.white_notes = ["C1", "D1", "E1", "F1", "G1", "A1", "B1",
                            "C2", "D2", "E2", "F2", "G2", "A2", "B2",
                            "C3", "D3", "E3", "F3", "G3", "A3", "B3",
                            "C4", "D4", "E4", "F4", "G4", "A4", "B4",
                            "C5", "D5", "E5", "F5", "G5", "A5", "B5",
                            "C6"]
        self.black_notes = ["C#1", "D#1", "F#1", "G#1", "A#1",
                            "C#2", "D#2", "F#2", "G#2", "A#2",
                            "C#3", "D#3", "F#3", "G#3", "A#3",
                            "C#4", "D#4", "F#4", "G#4", "A#4",
                            "C#5", "D#5", "F#5", "G#5", "A#5"]

        self.black_key_offsets = [1, 2, 4, 5, 6]
        self.pressed_keys = set()
        self.pressed_note = None

        self.sound_map = {}
        self.load_sounds()
        self.setMinimumHeight(200)

        piano_layout = QHBoxLayout()
        piano_layout.setContentsMargins(0, 0, 0, 0)
        piano_layout.setSpacing(0)
        self.setLayout(piano_layout)

    def load_sounds(self):
        """Загрузка звуков в словарь."""
        notes = self.white_notes + self.black_notes
        for note in notes:
            file_path = SOUND_PATH + note + ".wav"
            try:
                self.sound_map[note] = pygame.mixer.Sound(file_path)
            except FileNotFoundError:
                logger.error(f"Звуковой файл {note}.wav не был найден")
            except pygame.error:
                logger.error(f"Не удалось загрузить звук {note}")



    def play_sound(self, note):
        """Проигрывание звука с учетом громкости."""
        if note in self.sound_map:
            try:
                sound = self.sound_map[note]
                sound.set_volume(self.volume_control.get_volume())
                sound.play()
                self.recorder.add_note_event(note)
            except Exception as e:
                logger.error(f"Ошибка при воспроизведении звука для {note}: {e}")


    def keyPressEvent(self, event: QKeyEvent):
        """Обработка нажатий клавиш."""
        key = hot_key.get(str(event.key()))
        note = key

        if note in self.white_notes or note in self.black_notes:
            if note in self.pressed_keys is True:
                return
            else:
                self.pressed_keys.add(note)

        self.key_pressed.emit(self.pressed_keys)

        # Проигрываем звук
        self.play_sound(note)

        self.update()

    def keyReleaseEvent(self, event):
        """Сбрасываем нажатие клавиш."""
        key = hot_key.get(str(event.key()))
        note = key

        if note in self.pressed_keys:
            self.pressed_keys.remove(note)
            self.key_pressed.emit(self.pressed_keys)

        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        """Обработка нажатий клавиш."""
        x, y = event.x(), event.y()
        width = self.width()
        height = self.height()
        white_key_width = width // self.num_white_keys
        black_key_width = int(white_key_width * 0.6)
        black_key_height = int(height * 0.6)

        note = None

        # Проверяем черные клавиши
        if y <= black_key_height:
            for i in range(self.num_black_keys):
                octave = i // 5
                black_key_x = (self.black_key_offsets[i % 5] + octave * 7) * white_key_width - black_key_width // 2
                if black_key_x <= x < black_key_x + black_key_width:
                    note = self.black_notes[i]

                    break

        # Проверяем белые клавиши
        if not note:
            white_key_index = x // white_key_width
            if 0 <= white_key_index < len(self.white_notes):
                note = self.white_notes[white_key_index]

        self.pressed_keys.add(note)
        self.pressed_note = note

        self.key_pressed.emit(self.pressed_keys)

        # Проигрываем звук
        if note:
            self.play_sound(note)

        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Сбрасываем нажатие клавиш."""
        self.pressed_keys.remove(self.pressed_note)
        self.key_pressed.emit(self.pressed_keys)

        self.update()

    def paintEvent(self, event):
        """Отрисовка клавиш."""
        painter = QPainter(self)
        width = self.width()
        height = self.height()

        white_key_width = width // self.num_white_keys
        black_key_width = int(white_key_width * 0.6)
        black_key_height = int(height * 0.6)

        # Рисуем белые клавиши
        for i, note in zip(range(self.num_white_keys), self.white_notes):
            color = QColor(220, 220, 220) if (note in self.pressed_keys) else QColor(255, 255, 255)
            painter.setBrush(color)
            painter.setPen(Qt.black)
            painter.drawRect(i * white_key_width, 0, white_key_width, height)

        # Рисуем черные клавиши
        for i, note in zip(range(self.num_black_keys), self.black_notes):
            octave = i // 5
            x = (self.black_key_offsets[i % 5] + octave * 7) * white_key_width - black_key_width // 2
            color = QColor(50, 50, 50) if (note in self.pressed_keys) else QColor(0, 0, 0)
            painter.setBrush(color)
            painter.setPen(Qt.black)
            painter.drawRect(x, 0, black_key_width, black_key_height)


    def highlight_key(self, midi_note):
        key_name = self.midi_to_key(midi_note)
        logger.debug(f"Подсветка клавиши: {key_name}")
        self.pressed_keys.add(key_name)
        self.play_sound(key_name)
        self.key_pressed.emit(self.pressed_keys)

        self.update()


    def release_key(self, midi_note):
        key_name = self.midi_to_key(midi_note)
        logger.debug(f"Снятие подсветки: {key_name}")
        self.pressed_keys.remove(key_name)
        self.key_pressed.emit(self.pressed_keys)

        self.update()

    def midi_to_key(self, midi_note):
        notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        note_name = notes[midi_note % 12]
        octave = (midi_note // 12) - 1
        return f"{note_name}{octave}"

import time
from PyQt5.QtCore import QThread, pyqtSignal
from pianoKeyboard import PianoKeyboard
from mido import MidiFile

class MidiPlayer(QThread):
    progress_update = pyqtSignal(int)
    time_update = pyqtSignal(float ,float)

    def __init__(self, path : str, piano_keyboard : PianoKeyboard):
        """
        Инициализируем класс воспроизведения MIDI.
        :param piano_keyboard: Экземпляр класса PianoKeyboard.
        """
        super().__init__()
        self.midi_path = path
        self.piano_keyboard = piano_keyboard
        self.elapsed_time = 0
        self.total_time = 0

    def run(self):
        """
        Воспроизводит MIDI-файл с подсветкой клавиш.
        :param midi_path: Путь к MIDI-файлу.
        """
        midi_file = MidiFile(self.midi_path)
        self.total_time = sum(msg.time for msg in midi_file)

        for message in midi_file.play():
            if message.type == 'note_on' and message.velocity > 0:
                note = message.note
                self.piano_keyboard.highlight_key(note)  # Подсветка клавиши
            elif message.type == 'note_off' or (message.type == 'note_on' and message.velocity == 0):
                note = message.note
                self.piano_keyboard.release_key(note)  # Снятие подсветки

            # Обновляем прогресс и время
            self.elapsed_time += message.time
            progress = int((self.elapsed_time / self.total_time) * 100)
            self.progress_update.emit(progress) # Отправляем сигнал для обновления прогресса
            self.time_update.emit(self.elapsed_time, self.total_time)

            time.sleep(0.01)  # Задержка для плавного отображения
        self.progress_update.emit(-1)
        self.time_update.emit(0, 0)
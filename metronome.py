import pygame
import time

TICK_PATH = "resources/tick/tick.wav"

class Metronome:
    def __init__(self, bpm=60, volume = 0.2):
        self.metronome_playing = False  # Переменная для отслеживания состояния метронома
        pygame.mixer.init()  # Инициализируем pygame для работы с аудио
        self.interval = 60 / bpm
        self.tick_sound = pygame.mixer.Sound(TICK_PATH)  # Звук тика
        self.tick_sound.set_volume(volume)


        # При нажатии на кнопку Metronome
    def on_tempo_button_click(self):
        if not self.metronome_playing:
            self.start_metronome()  # Запускаем метроном
        else:
            self.stop_metronome()  # Останавливаем метроном

    def start_metronome(self):
        """Запускаем метроном с заданным темпом (BPM)."""
        self.metronome_playing = True

        # Функция для воспроизведения метронома
        def play_metronome():
            while self.metronome_playing:
                self.tick_sound.play()  # Воспроизводим звук удара метронома
                time.sleep(self.interval)  # Ждем до следующего удара

        # Запускаем метроном в фоновом потоке
        import threading
        threading.Thread(target=play_metronome, daemon=True).start()

    def stop_metronome(self):
        """Останавливаем метроном."""
        self.metronome_playing = False

    def update_data(self, new_bpm, new_volume):
        """Обновление данных для метронома (BPM и громкость)."""
        self.stop_metronome()  # Останавливаем метроном перед изменением параметров
        self.interval = 60 / new_bpm  # Обновляем интервал
        self.tick_sound.set_volume(new_volume)  # Обновляем громкость
        self.start_metronome()  # Перезапускаем метроном с новыми параметрами


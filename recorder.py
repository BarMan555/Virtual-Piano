import os
import wave
import time
import pygame
from mido import MidiFile, MidiTrack, Message
import numpy as np
from loguru import logger
from datetime import datetime

SOUND_PATH = "sounds/"

class Recorder:
    def __init__(self, record_folder="record"):
        self.recording = False
        self.notes = []
        self.start_time = None
        self.record_folder = record_folder

        # Создаем папку для записей, если её нет
        if not os.path.exists(self.record_folder):
            os.makedirs(self.record_folder)

    # При нажатии на кнопку Record
    def toggle_recording(self):
        """Переключение состояния записи."""
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """Начинаем запись."""
        self.recording = True
        self.notes = []
        self.start_time = time.time()
        logger.info("Запись началась.")

    def stop_recording(self):
        """Останавливаем запись."""
        self.recording = False
        logger.info("Запись завершена.")
        self.save_to_wav()
        self.save_to_midi()

    def add_note_event(self, note):
        """Добавляем событие нажатия ноты."""
        if self.recording:
            current_time = time.time()
            timestamp = current_time - self.start_time
            self.notes.append((note, timestamp))
            logger.debug(f"Нота {note} добавлена в {timestamp:.2f} секунд.")

    def save_to_wav(self):
        """Сохраняем записанную мелодию в WAV."""
        if not self.notes:
            logger.warning("Ничего не было записанно")
            return
        file_name = f"{self.record_folder}/record_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"

        # Параметры записи
        sample_rate = 44100
        samples = np.zeros(0, dtype=np.float32)  # Итоговый аудиомассив
        last_time = 0  # Последняя временная отметка

        for i, (note, timestamp) in enumerate(self.notes):
            # Загружаем звук ноты
            sound = pygame.mixer.Sound(SOUND_PATH + note + ".wav")
            raw_samples = pygame.sndarray.array(sound).astype(np.float32)

            # Убедимся, что массив одномерный (конвертация стерео в моно, если нужно)
            if raw_samples.ndim == 2:
                raw_samples = raw_samples.mean(axis=1)

            # Продолжительность звучания ноты
            duration = (self.notes[i + 1][1] - timestamp) if i + 1 < len(self.notes) else 1.0  # Длительность (по умолчанию 1 секунда)
            num_samples = int(sample_rate * duration)
            trimmed_samples = raw_samples[:num_samples]  # Обрезаем по длительности

            # Добавляем паузу, если есть разрыв между звуками
            silence_duration = timestamp - last_time
            silence_samples = np.zeros(int(sample_rate * silence_duration), dtype=np.float32)
            samples = np.concatenate((samples, silence_samples, trimmed_samples))

            last_time = timestamp + duration  # Обновляем последнюю временную отметку

        # Нормализация амплитуды
        if np.max(np.abs(samples)) > 0:
            samples = samples / np.max(np.abs(samples))

        # Сохраняем в WAV
        with wave.open(file_name, "w") as wav_file:
            wav_file.setnchannels(1)  # Моно
            wav_file.setsampwidth(2)  # 16 бит
            wav_file.setframerate(sample_rate)
            wav_file.writeframes((samples * 32767).astype(np.int16).tobytes())

        logger.success(f"WAV Файл сохранён: {file_name}")

    def save_to_midi(self):
        """Сохраняем записанную мелодию в MIDI файл."""
        if not self.notes:
            logger.warning("Ничего не было записанно")
            return
        file_name = f"{self.record_folder}/record_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mid"
        midi_file = MidiFile()
        track = MidiTrack()
        midi_file.tracks.append(track)

        # Установим инструмент, например, фортепиано
        track.append(Message('program_change', program=0, time=0))

        # Перебираем записанные ноты и вычисляем их длительность
        for i, (note, timestamp) in enumerate(self.notes):
            note_num = self.note_to_midi(note)  # Конвертируем ноту в MIDI-номер
            # Определяем временную разницу между нотами (в тиках MIDI)
            if i == 0:
                delta_time = 0  # Первая нота начинается сразу
            else:
                delta_time = int((self.notes[i][1] - self.notes[i - 1][1]) * 480)  # Время в тиках между нотами

            # Добавляем событие начала ноты
            track.append(Message('note_on', note=note_num, velocity=64, time=delta_time))

            # Определяем длительность ноты
            if i + 1 < len(self.notes):
                duration = int((self.notes[i + 1][1] - timestamp) * 480)  # Длительность до следующей ноты
            else:
                duration = 480  # Последняя нота длится 1/4 такта (по умолчанию)

            # Добавляем событие завершения ноты
            track.append(Message('note_off', note=note_num, velocity=64, time=duration))

        # Сохраняем файл
        midi_file.save(file_name)
        logger.success(f"MIDI файл сохранен: {file_name}")

    def note_to_midi(self, note):
        """
        Конвертируем название ноты (с указанием октавы) в MIDI-номер.
        Поддерживаются ноты от C1 до C5.
        """
        note_map = {
            "C": 0,
            "C#": 1,
            "D": 2,
            "D#": 3,
            "E": 4,
            "F": 5,
            "F#": 6,
            "G": 7,
            "G#": 8,
            "A": 9,
            "A#": 10,
            "B": 11
        }

        # Извлекаем название ноты и номер октавы
        try:
            base_note = note[:-1]  # Например, "C4" -> "C"
            octave = int(note[-1])  # Например, "C4" -> 4
            midi_number = 12 * (octave + 1) + note_map[base_note]
            return midi_number
        except (KeyError, ValueError):
            # Возвращаем ноту C4 (60), если данные некорректны
            return 60

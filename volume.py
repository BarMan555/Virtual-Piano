import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSlider, QPushButton, QWidget, QHBoxLayout, \
    QSizePolicy, QGridLayout, QAction, QStyle
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QMouseEvent
import pygame.mixer

from recorder import Recorder
from metronome import Metronome
from menuBar import MenuBar
from pianoControlPanel import PianoControlPanel
from pianoKeyboard import PianoKeyboard

class VolumeControl:
    """Класс для управления громкостью."""
    def __init__(self):
        self.volume = 0.5

    def set_volume(self, value):
        self.volume = value / 100

    def get_volume(self):
        return self.volume
from PyQt5.QtWidgets import QSlider, QPushButton, QWidget, QHBoxLayout, \
    QSizePolicy, QGridLayout
from PyQt5.QtCore import Qt

class PianoControlPanel(QWidget):
    def __init__(self, volume_control, recorder, metronome):
        super().__init__()

        self.volume_control = volume_control
        self.recorder = recorder
        self.metronome = metronome

        control_panel = QWidget() # Main widget for Control Panel
        control_layout = QHBoxLayout() # Main layout for Control Panel

        volume_slider = self.make_slider()
        buttons_menu = self.make_buttons_menu()

        control_layout.setSpacing(50)
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.setAlignment(Qt.AlignCenter)
        control_layout.addWidget(volume_slider)
        control_layout.addWidget(buttons_menu)

        control_panel.setLayout(control_layout)
        self.setLayout(control_layout)

    def change_volume(self, value):
        """Обновляем громкость."""
        self.volume_control.set_volume(value)

    def make_slider(self):
        volume_slider = QSlider(Qt.Vertical)
        volume_slider.setRange(0, 100)
        volume_slider.setValue(50)
        volume_slider.setTickPosition(QSlider.TicksBothSides)
        volume_slider.setTickInterval(25)
        volume_slider.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        volume_slider.valueChanged.connect(self.change_volume)
        return volume_slider

    def make_buttons_menu(self):

        record_button = QPushButton("Record")
        record_button.clicked.connect(self.recorder.toggle_recording)

        change_voice_button = QPushButton("Change Voice")

        tempo_button = QPushButton("Metronome")
        tempo_button.clicked.connect(self.metronome.on_tempo_button_click)

        change_voice_button3 = QPushButton("Change Voice")

        button_grid = QGridLayout()
        button_grid.setSpacing(5)
        button_grid.addWidget(record_button, 0, 0)
        button_grid.addWidget(change_voice_button, 0, 1)
        button_grid.addWidget(tempo_button, 1, 0)
        button_grid.addWidget(change_voice_button3, 1, 1)

        buttons_menu = QWidget()
        buttons_menu.setLayout(button_grid)
        return buttons_menu
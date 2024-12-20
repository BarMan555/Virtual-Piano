import time

from PyQt5.QtWidgets import QSlider, QPushButton, QWidget, QHBoxLayout, \
    QSizePolicy, QGridLayout, QLabel, QFileDialog, QProgressBar, QVBoxLayout
from PyQt5.QtCore import Qt
from midiPlayer import MidiPlayer

class PianoControlPanel(QWidget):
    def __init__(self, volume_control, recorder, metronome, piano_panel):
        super().__init__()

        self.is_recording = False;

        self.volume_control = volume_control
        self.recorder = recorder
        self.metronome = metronome
        self.piano_panel = piano_panel

        control_panel = QWidget() # Main widget for Control Panel
        control_layout = QHBoxLayout() # Main layout for Control Panel

        volume_slider = self.make_slider()
        buttons_menu = self.make_buttons_menu()
        self.text_display, self.keys_display = self.make_key_display()
        self.progress_bar = self.make_progress_bar()
        self.time_label = self.make_time_label()

        display_layout = QVBoxLayout()
        display_layout.addWidget(self.text_display)
        display_layout.addWidget(self.keys_display)
        display_widget = QWidget(self)
        display_widget.setLayout(display_layout)

        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.time_label)
        progress_widget = QWidget(self)
        progress_widget.setLayout(progress_layout)

        record_layout = QVBoxLayout()
        record_layout.addWidget(buttons_menu)
        record_layout.addWidget(progress_widget)
        record_widget = QWidget(self)
        record_widget.setLayout(record_layout)

        control_layout.setSpacing(50)
        control_layout.setContentsMargins(10, 10, 10, 10)
        control_layout.addWidget(volume_slider)
        control_layout.addWidget(display_widget)
        control_layout.addWidget(record_widget)

        control_panel.setLayout(control_layout)
        self.setLayout(control_layout)

    def change_volume(self, value):
        """Обновляем громкость."""
        self.volume_control.set_volume(value)

    def make_key_display(self):
        text_label = QLabel("Нажатые клавиши: ", self)
        pressed_keys_label = QLabel("", self)
        pressed_keys_label.setWordWrap(True)
        pressed_keys_label.setFixedWidth(200)

        text_label.setAlignment(Qt.AlignCenter)
        pressed_keys_label.setAlignment(Qt.AlignCenter)

        text_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        pressed_keys_label.setStyleSheet("font-size: 25px; font-weight: bold;")
        return text_label, pressed_keys_label

    def make_slider(self):
        volume_slider = QSlider(Qt.Vertical)
        volume_slider.setRange(0, 100)
        volume_slider.setValue(50)
        volume_slider.setTickPosition(QSlider.TicksBothSides)
        volume_slider.setTickInterval(25)
        volume_slider.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        volume_slider.valueChanged.connect(self.change_volume)

        volume_slider.setStyleSheet("""
            QSlider::handle::vertical {
                background: #888;
                border: 1px solid #666;
                width: 14px;
                height: 14px;
                margin: 0 -3px;
                border-radius: 7px;
            }
        """)
        return volume_slider

    def make_progress_bar(self):
        progress_bar = QProgressBar(self)
        progress_bar.setValue(0)
        progress_bar.setTextVisible(False)
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #34495E;
                border-radius: 10px;
                background: #BDC3C7;
            }

            QProgressBar::chunk {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #2ECC71, stop: 1 #27AE60
                );
                border-radius: 10px;
            }
        """)
        return progress_bar


    def make_time_label(self):
        time_label = QLabel("0.0/0.0c", self)
        time_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        return time_label


    def make_buttons_menu(self):
        self.buttons = []
        for i in range(3):
            button = QPushButton("")
            button.setStyleSheet("""
                QPushButton {
                    background-color: white;      /* Зеленый фон */
                    color: black;                  /* Белый текст */
                    border: 2px solid gray;     /* Рамка */
                    border-radius: 5px;            /* Закругленные углы */
                    padding: 3px;                  /* Внутренний отступ */
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: gray;     /* Более темный зеленый при наведении */
                    color: white
                }
                QPushButton:pressed {
                    background-color: #36732d;     /* Темно-зеленый при нажатии */
                }
            """)
            self.buttons.append(button)


        self.buttons[0].setText("Record")
        self.buttons[0].clicked.connect(self.restyle_record_button)

        self.buttons[1].setText("Midi Player")
        self.buttons[1].clicked.connect(self.open_midi_file)

        self.buttons[2].setText("Metronome")
        self.buttons[2].clicked.connect(self.metronome.on_tempo_button_click)


        button_grid = QGridLayout()
        button_grid.setSpacing(5)
        button_grid.addWidget(self.buttons[0], 0, 0)
        button_grid.addWidget(self.buttons[1], 1, 1)
        button_grid.addWidget(self.buttons[2], 1, 0)

        buttons_menu = QWidget()
        buttons_menu.setLayout(button_grid)
        return buttons_menu


    def restyle_record_button(self):
        if not self.is_recording:
            self.is_recording = True
            self.buttons[0].setStyleSheet("""
                QPushButton {
                            background-color: red;      /* Зеленый фон */
                            color: white;                  /* Белый текст */
                            border: 2px solid gray;     /* Рамка */
                            border-radius: 5px;            /* Закругленные углы */
                            padding: 3px;                  /* Внутренний отступ */
                            font-size: 16px;
                        }
                        QPushButton:hover {
                            background-color: gray;     /* Более темный зеленый при наведении */
                            color: white
                        }
                        QPushButton:pressed {
                            background-color: #36732d;     /* Темно-зеленый при нажатии */
                        }
            """)
        else:
            self.is_recording = False
            self.buttons[0].setStyleSheet("""
                            QPushButton {
                                        background-color: white;      /* Зеленый фон */
                                        color: black;                  /* Белый текст */
                                        border: 2px solid gray;     /* Рамка */
                                        border-radius: 5px;            /* Закругленные углы */
                                        padding: 3px;                  /* Внутренний отступ */
                                        font-size: 16px;
                                    }
                                    QPushButton:hover {
                                        background-color: gray;     /* Более темный зеленый при наведении */
                                        color: white
                                    }
                                    QPushButton:pressed {
                                        background-color: #36732d;     /* Темно-зеленый при нажатии */
                                    }
                        """)
        self.recorder.toggle_recording()


    def update_pressed_keys(self, pressed_keys):
        if pressed_keys:
            self.keys_display.setText(", ".join(pressed_keys))
        else:
            self.keys_display.setText("")

    def open_midi_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите MIDI файл", "", "MIDI Files (*.mid)",
                                                   options=options)
        self.midi_thread = MidiPlayer(file_path, self.piano_panel)
        if file_path:
            self.progress_bar.setValue(0)
            self.midi_thread.progress_update.connect(self.update_progress_bar)
            self.midi_thread.time_update.connect(self.update_time_label)
            self.midi_thread.start()

    def update_progress_bar(self, progress):
        if progress == -1:
            time.sleep(1)
            self.progress_bar.setValue(0)
        self.progress_bar.setValue(progress)


    def update_time_label(self, elapsed_time, total_time):
        self.time_label.setText(f"{elapsed_time:.1f}/{total_time:.1f}s")

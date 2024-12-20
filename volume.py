class VolumeControl:
    """Класс для управления громкостью."""
    def __init__(self):
        self.volume = 0.5

    def set_volume(self, value):
        self.volume = value / 100

    def get_volume(self):
        return self.volume
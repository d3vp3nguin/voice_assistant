class Settings():
    """Класс для настроек голосового ассистента"""

    def __init__(self, rate, volume, voice, pause_threshold):
        self.rate = rate
        self.volume = volume
        self.voice = voice
        self.pause_threshold = pause_threshold

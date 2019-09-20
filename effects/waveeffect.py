from effects.effect import Effect
from bulbs.pulsebulb import PulseBulb

class WaveEffect(Effect):
    def __init__(self, minbrightness = 0, maxbrightness = 1, delay = 10):
        Effect.__init__(self)
        self.delay = delay
        self.minbrightness = minbrightness
        self.maxbrightness = maxbrightness
        
    def initialize(self, matrix):
        self._matrix = matrix
        for col in range(self._matrix.columns):
            for row in range(self._matrix.rows):
                bulb = PulseBulb(delay = self.delay, minbrightness = self.minbrightness, maxbrightness = self.maxbrightness)
                bulb.brightness = col * (self.maxbrightness - self.minbrightness) / self._matrix.columns
                self._matrix.add(bulb, col, row)
from effects.effect import Effect
from bulbs.blinkbulb import BlinkBulb

class BlinkColumnEffect(Effect):
    def __init__(self, on_length = 1, off_length = 1, maxbrightness = 1):
        Effect.__init__(self)
        self._on_length = on_length
        self._off_length = off_length
        self._maxbrightness = maxbrightness
        
    def initialize(self, matrix):
        self._matrix = matrix
        for col in range(self._matrix.columns):
            for row in range(self._matrix.rows):
                bulb = BlinkBulb(on_length = self._on_length, off_length=self._off_length, maxbrightness=self._maxbrightness, initialstate = col % 2)
                self._matrix.add(bulb, col, row)
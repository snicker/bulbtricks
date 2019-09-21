from effects.effect import Effect, EffectCycler
from bulbs.blinkbulb import BlinkBulb

class BlinkEffect(Effect):
    def __init__(self, on_length = 1, off_length = 1, maxbrightness = 1):
        Effect.__init__(self)
        self._on_length = on_length
        self._off_length = off_length
        self._maxbrightness = maxbrightness
        
    def initialize(self, matrix):
        self._matrix = matrix
        for col in range(self._matrix.columns):
            for row in range(self._matrix.rows):
                bulb = BlinkBulb(on_length = self._on_length, off_length=self._off_length, maxbrightness=self._maxbrightness)
                self._matrix.add(bulb, col, row)

class BlinkColumnEffect(BlinkEffect):        
    def initialize(self, matrix):
        self._matrix = matrix
        for col in range(self._matrix.columns):
            for row in range(self._matrix.rows):
                bulb = BlinkBulb(on_length = self._on_length, off_length=self._off_length, maxbrightness=self._maxbrightness, initialstate = col % 2)
                self._matrix.add(bulb, col, row)

class BlinkRowEffect(BlinkEffect):
    def initialize(self, matrix):
        self._matrix = matrix
        for col in range(self._matrix.columns):
            for row in range(self._matrix.rows):
                bulb = BlinkBulb(on_length = self._on_length, off_length=self._off_length, maxbrightness=self._maxbrightness, initialstate = row % 2)
                self._matrix.add(bulb, col, row)
                
class BlinkCycleEffect(EffectCycler):
    def __init__(self, on_length = 1, off_length = 1, maxbrightness = 1, cycles_per_effect = 2):
        EffectCycler.__init__(self)
        effect_length = (on_length + off_length) * cycles_per_effect
        blinkargs = {'on_length': on_length, 'off_length': off_length, 'maxbrightness': maxbrightness}
        self.add_effect(BlinkEffect(**blinkargs), effect_length)
        self.add_effect(BlinkRowEffect(**blinkargs), effect_length)
        self.add_effect(BlinkColumnEffect(**blinkargs), effect_length)
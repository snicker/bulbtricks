from effects.effect import Effect, EffectCycler
from bulbs.pulsebulb import PulseBulb

class PulseEffect(Effect):
    def __init__(self, pulse_length = 2, minbrightness = 0, maxbrightness = 1):
        Effect.__init__(self)
        self._pulse_length = pulse_length
        self._minbrightness = minbrightness
        self._maxbrightness = maxbrightness

    def _get_effect_bulb(self):
        bulb = PulseBulb(delay = self._pulse_length / 2.0, minbrightness = self._minbrightness, maxbrightness = self._maxbrightness)
        
    def initialize(self, matrix):
        self._matrix = matrix
        for col in range(self._matrix.columns):
            for row in range(self._matrix.rows):
                bulb = self._get_effect_bulb()
                self._matrix.add(bulb, col, row)

class PulseColumnEffect(PulseEffect):        
    def initialize(self, matrix):
        self._matrix = matrix
        for col in range(self._matrix.columns):
            for row in range(self._matrix.rows):
                bulb = self._get_effect_bulb()
                if col % 2 == 1:
                    bulb.brightness = self._maxbrightness
                self._matrix.add(bulb, col, row)

class PulseRowEffect(PulseEffect):
    def initialize(self, matrix):
        self._matrix = matrix
        for col in range(self._matrix.columns):
            for row in range(self._matrix.rows):
                bulb = self._get_effect_bulb()
                if row % 2 == 1:
                    bulb.brightness = self._maxbrightness
                self._matrix.add(bulb, col, row)
                
class PulseCycleEffect(EffectCycler):
    def __init__(self, pulse_length = 2, minbrightness = 0, maxbrightness = 1, cycles_per_effect = 2):
        EffectCycler.__init__(self)
        effect_length = pulse_length * cycles_per_effect
        pulseargs = {'pulse_length': pulse_length, 'minbrightness': minbrightness, 'maxbrightness': maxbrightness}
        self.add_effect(PulseEffect(**pulseargs), effect_length)
        self.add_effect(PulseRowEffect(**pulseargs), effect_length)
        self.add_effect(PulseColumnEffect(**pulseargs), effect_length)
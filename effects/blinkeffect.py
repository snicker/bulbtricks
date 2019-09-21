from effects.effect import Effect
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
                
class BlinkCycleEffect(BlinkEffect):
    def __init__(self, on_length = 1, off_length = 1, maxbrightness = 1, cycles_per_effect = 2):
        blinkargs = {'on_length': on_length, 'off_length': off_length, 'maxbrightness': maxbrightness}
        BlinkEffect.__init__(self, **blinkargs)
        self._cycles_per_effect = cycles_per_effect
        self._current_effect = None
        self._effect_order = []
        self._effect_order.append(BlinkEffect(**blinkargs))
        self._effect_order.append(BlinkRowEffect(**blinkargs))
        self._effect_order.append(BlinkColumnEffect(**blinkargs))
        
    def initialize(self, matrix):
        self._matrix = matrix
        self.next_effect()
        
    def step(self):
        self.next_effect()
        
    def next_effect(self):
        if self._current_effect:
            self._matrix.remove(self._current_effect)
        self._current_effect = self._effect_order.pop(0)
        self._effect_order.append(self._current_effect)
        self._matrix.add_effect(self._current_effect)
        self.next_step_in((self._on_length + self._off_length) * self._cycles_per_effect)
        
    def remove(self):
        if self._current_effect:
            self._matrix.remove(self._current_effect)
        
        
        
        
class Effect:
    def __init__(self):
        self._matrix = None
        self._ticks_per_step = 1
        self._ticks = 0
        
    def initialize(self, matrix):
        self._matrix = matrix
        
    def remove(self):
        pass
        
    def next_step_in(self, seconds):
        if self._matrix:
            self._ticks = 0
            self._ticks_per_step = int(seconds * self._matrix.frequency) - 1
        
    def tick(self):
        self._ticks += 1
        if self._ticks >= self.ticks_per_step:
            self._ticks = 0
            self.step()
        
    def step(self):
        pass

    @property
    def ticks_per_step(self):
        return self._ticks_per_step
        
    @property
    def completed(self):
        return False
        
    def on_completed(self):
        return lambda: None

class EffectCycler(Effect):
    def __init__(self):
        Effect.__init__(self)
        self._current_effect = None
        self._effect_order = []

    def add_effect(self, effect, length = 1):
        self._effect_order.append({'effect': effect, 'length': length})
        
    def initialize(self, matrix):
        self._matrix = matrix
        self.next_effect()
        
    def step(self):
        self.next_effect()
        
    def next_effect(self):
        if self._current_effect:
            self._matrix.remove_effect(self._current_effect['effect'])
        self._current_effect = self._effect_order.pop(0)
        self._effect_order.append(self._current_effect)
        self._matrix.add_effect(self._current_effect['effect'])
        self.next_step_in(self._current_effect['length'])
        
    def remove(self):
        if self._current_effect:
            self._matrix.remove_effect(self._current_effect['effect'])
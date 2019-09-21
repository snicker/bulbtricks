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
            self._ticks_per_step = int(seconds * self._matrix.frequency)
        
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

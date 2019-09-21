from bulbtricks.bulbs.bulb import Bulb

class BlinkBulb(Bulb):
    def __init__(self, on_length = 1, off_length = 1, maxbrightness = 1, initialstate = 0):
        Bulb.__init__(self)
        self._state = initialstate
        self._on_length = on_length
        self._off_length = off_length
        self._maxbrightness = maxbrightness
        self.set_state(self._state)
        
    @property
    def maxbrightness(self):
        return self._maxbrightness
        
    @property
    def on_length(self):
        return self._on_length

    @property
    def off_length(self):
        return self._off_length
        
    @property
    def state(self):
        return self._state
        
    def set_state(self, state):
        self._state = state
        if self._state:
            self.brightness = self.maxbrightness
            self.next_step_in(self.on_length)
        else:
            self.brightness = 0
            self.next_step_in(self.off_length)
        
    def step(self, direction):
        self.set_state(abs(self.state - 1))
        
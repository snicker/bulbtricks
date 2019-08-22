from bulbs.bulb import Bulb

class RampUpBulb(Bulb):
    def __init__(self, delay = 3):
        Bulb.__init__(self)
        self._delay = delay
        
    @property
    def delay(self):
        return self._delay
        
    def step(self, direction):
        self.brightness += self.speed * direction * 1.0 / (self.delay * self.frequency / self.ticks_per_step)
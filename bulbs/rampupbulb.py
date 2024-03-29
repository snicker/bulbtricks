from bulbtricks.bulbs.bulb import Bulb

class RampUpBulb(Bulb):
    def __init__(self, minbrightness = 0, maxbrightness = 1, delay = 3):
        Bulb.__init__(self)
        self._delay = delay
        self._minbrightness = minbrightness
        self._maxbrightness = maxbrightness
        
    @property
    def minbrightness(self):
        return self._minbrightness

    @property
    def maxbrightness(self):
        return self._maxbrightness
        
    @property
    def delay(self):
        return self._delay
        
    def step(self, direction):
        self.brightness += self.speed * direction * (self.maxbrightness - self.minbrightness) / (self.delay * self.frequency / self.ticks_per_step)
        if self.brightness >= self.maxbrightness or self.brightness <= self.minbrightness:
            self.brightness = max(self.minbrightness,min(self.maxbrightness,self.brightness))
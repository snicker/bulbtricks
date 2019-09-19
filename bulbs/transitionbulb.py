from bulbs.bulb import Bulb

class TransitionBulb(Bulb):
    def __init__(self, frombulb = None, tobulb = None, delay = 3):
        Bulb.__init__(self)
        self._frombulb = frombulb
        self._tobulb = tobulb
        self._delay = delay
        self.brightness = self.startingbrightness
        
    @property
    def completed(self):
        return (self.startingbrightness >= self.endingbrightness and self.brightness <= self.endingbrightness) or (self.endingbrightness >= self.startingbrightness and self.brightness >= self.endingbrightness)
        
    @property
    def delay(self):
        return self._delay
        
    @property
    def startingbrightness(self):
        return self._frombulb.brightness if self._frombulb else 0
        
    @property
    def endingbrightness(self):
        return self._tobulb.brightness if self._tobulb else 1
        
    def step(self, direction):
        if self.startingbrightness >= self.endingbrightness:
            direction *= -1
        self.brightness += self.speed * direction * abs(self.startingbrightness - self.endingbrightness) / (self.delay * self.frequency / self.ticks_per_step)
        if self.completed:
            self.brightness = self.endingbrightness
        
        
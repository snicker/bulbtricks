from bulbs.rampupbulb import RampUpBulb

class PulseBulb(RampUpBulb):
    def __init__(self, minbrightness = 0, maxbrightness = 1, delay = 3):
        RampUpBulb.__init__(self, minbrightness=minbrightness, maxbrightness=maxbrightness, delay=delay)
        self._pulse_direction = 1
        
    @property
    def pulsedirection(self):
        return self._pulse_direction
        
    def step(self, direction):
        self.brightness += self.speed * direction * (self.maxbrightness - self.minbrightness) / (self.delay * self.frequency / self.ticks_per_step)
        if self.brightness >= self.maxbrightness or self.brightness <= self.minbrightness:
            self.brightness = max(self.minbrightness,min(self.maxbrightness,self.brightness))
            self._pulse_direction *= -1
        
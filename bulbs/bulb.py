class Bulb:
    def __init__(self):
        self._brightness = 0.0
        self._ticks = 0
        self._ticks_per_step = 1
        self._direction = 1
        self._speed = 1.0
        self._frequency = 240
        
    @property
    def frequency(self):
        return self._frequency

    @property
    def speed(self):
        return self._speed
        
    @property
    def direction(self):
        return self._direction
        
    @property
    def ticks_per_step(self):
        return self._ticks_per_step
        
    @property
    def brightness(self):
        return self._brightness
        
    @brightness.setter
    def brightness(self, brightness):
        if brightness < 0:
            self._brightness = 0
        elif brightness > 1:
            self._brightness = 1
        else:
            self._brightness = brightness
        
    def reverse(self):
        self._direction *= -1
        
    def forward(self):
        self._direction = 1
        
    def backward(self):
        self._direction = -1
        
    def tick(self):
        self._ticks += 1
        if self._ticks >= self.ticks_per_step:
            self._ticks = 0
            self.step(self._direction)
            
    def step(self, direction):
        pass
class Filter(object):
    def __init__(self, filtered):
        self._filtered = filtered
        
    def __getattr__(self, attr):
        if attr in ['tick', 'step'] + self.filtered_properties:
            return self.brightness
        return self._filtered.__getattr__(attr)
        
    @property
    def filtered_properties(self):
        return ['brightness']
        
    @property
    def original(self):
        return self._filtered
        
    @property
    def brightness(self):
        return self._filtered.brightness
        
    @brightness.setter
    def brightness(self, value):
        self._filtered.brightness = value
        
    def tick(self):
        self.filter_tick()
        self._filtered.tick()
        
    def step(self, direction):
        self.filter_step(self, direction)
        self._filtered.step(direction)
        
    def filter_tick(self):
        pass
        
    def filter_step(self):
        pass
       
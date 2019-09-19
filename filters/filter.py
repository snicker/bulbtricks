class Filter(object):
    def __init__(self, filtered):
        self._filtered = filtered
        
    def __getattr__(self, attr):
        if attr in self.filtered_properties:
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
       
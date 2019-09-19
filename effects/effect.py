class Effect:
    def __init__(self):
        self._matrix = None
        
    def initialize(self, matrix):
        self._matrix = matrix
        
    def remove(self):
        pass
        
    def tick(self):
        pass
        
    @property
    def completed(self):
        return False
        
    def on_completed(self):
        return lambda: None

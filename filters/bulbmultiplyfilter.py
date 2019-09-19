from filters.filter import Filter

class BulbMultiplyFilter(Filter):
    def __init__(self, filtered, bulb):
        Filter.__init__(self, filtered)
        self.bulb = bulb
        
    def filter_tick(self)
        self.bulb.tick()
    
    @property
    def brightness(self):
        return self.original.brightness * self.bulb.brightness
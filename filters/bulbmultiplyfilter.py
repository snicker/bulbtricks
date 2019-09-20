from filters.filter import Filter

class BulbMultiplyFilter(Filter):
    def __init__(self, filtered, bulb):
        Filter.__init__(self, filtered)
        self.bulb = bulb
        self.multiplier = 1
        
    def filter_tick(self):
        self.bulb.tick()
    
    @property
    def brightness(self):
        return max(0,min(1,self.original.brightness * self.bulb.brightness * self.multiplier))
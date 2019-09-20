from effects.effect import Effect
from bulbs.rampupbulb import RampUpBulb
from bulbs.transitionbulb import TransitionBulb
from bulbs.bulb import Bulb
from filters.bulbmultiplyfilter import BulbMultiplyFilter
import copy

class HighlightEffect(Effect):
    def __init__(self, column, row, minbrightnessmodifier = 0.01, maxbrightnessmodifier = 1, delay = 3):
        Effect.__init__(self)
        self.delay = delay
        self.column = column
        self.row = row
        self.minbrightnessmodifier = minbrightnessmodifier
        self.maxbrightnessmodifier = maxbrightnessmodifier
        
    @property
    def completed(self):
        return True
        
    def on_completed(self):
        return lambda: self._matrix.add_effect(HighlightEffect_Up(self))
        
class HighlightEffect_Up(Effect):
    def __init__(self, options):
        self.options = options
        self.transitionbulb = None
        self.filtered = []
        self.focusbulb = None
        
    @property
    def completed(self):
        return self.transitionbulb and self.transitionbulb.completed
    
    def on_completed(self):
        return lambda: self._matrix.add_effect(HighlightEffect_Down(self.options))
    
    def get_mbulb(self):
        mbulb = RampUpBulb(delay = self.options.delay / 2, maxbrightness = self.options.maxbrightnessmodifier, minbrightness = self.options.minbrightnessmodifier)
        mbulb.reverse()
        mbulb.brightness = self.options.maxbrightnessmodifier
        return mbulb
        
    def get_fbulb(self, bulb):
        mbulb = self.get_mbulb()
        return BulbMultiplyFilter(bulb, mbulb)
        
    def get_tbulb(self, frombulb):
        tobulb = Bulb()
        tobulb.brightness = 1
        return TransitionBulb(delay = self.options.delay / 2, frombulb = frombulb, tobulb = tobulb)
    
    def initialize(self, matrix):
        self._matrix = matrix
        self.filtered = []
        self.focusbulb = self._matrix.at(self.options.column, self.options.row)
        for column in range(self._matrix.columns):
            for row in range(self._matrix.rows):
                bulb = self._matrix.at(column, row)
                if bulb not in self.filtered:
                    fbulb = self.get_fbulb(bulb)
                    self.filtered.append(fbulb)
                    self._matrix.replace(bulb, fbulb)
        self.transitionbulb = self.get_tbulb(self.focusbulb)
        self._matrix.add(self.transitionbulb, self.options.column, self.options.row)
                    
    def remove(self):
        for fbulb in self.filtered:
            self._matrix.replace(fbulb, fbulb.original)
        self._matrix.replace(self.transitionbulb, self.focusbulb)

class HighlightEffect_Down(HighlightEffect_Up):
    def on_completed(self):
        return lambda: None

    def get_mbulb(self):
        return RampUpBulb(delay = self.options.delay / 2, maxbrightness = self.options.maxbrightnessmodifier, minbrightness = self.options.minbrightnessmodifier)
        
    def get_tbulb(self, frombulb):
        tobulb = Bulb()
        tobulb.brightness = 1
        return TransitionBulb(delay = self.options.delay / 2, frombulb = tobulb, tobulb = frombulb)

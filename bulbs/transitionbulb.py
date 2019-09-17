from bulbs.rampupbulb import RampUpBulb

class TransitionBulb(RampUpBulb):
    def __init__(self, frombulb = None, tobulb = None, delay = 3):
        RampUpBulb.__init__(self, minbrightness=0, maxbrightness=1, delay=delay)
        self._frombulb = frombulb
        self._tobulb = tobulb
        
    @property
    def minbrightness(self):
        return self._frombulb.brightness if self._frombulb else 0
        
    @property
    def maxbrightness(self):
        return self._tobulb.brightness if self._tobulb else 1
        
        
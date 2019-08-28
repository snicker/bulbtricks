import time, sched
import threading
import logging

class DisplayDriver:
    def __init__(self, matrix):
        self.frequency = 30
        self.running = False
        self.matrix = matrix
        self._scheduler_thread = None
    
    def run(self):
        if not self.running:
            scheduler = sched.scheduler(time.time, time.sleep)
            self.running = True
            self.on_start()
            def fn():
                if self.running:
                    scheduler.enter(1.0 / self.frequency, 0, fn, ())
                self.render()
            def fn_start():
                scheduler.enter(1.0 / self.frequency, 0, fn, ())
                scheduler.run()
            self._scheduler_thread = threading.Thread(target = fn_start)
            self._scheduler_thread.start()
        
    def stop(self):
        self.running = False
        self.on_stop()
        if self._scheduler_thread:
            self._scheduler_thread.join()
            self._scheduler_thread = None
            
    def on_start(self):
        pass
        
    def on_stop(self):
        pass
        
    def render(self):
        pass
        
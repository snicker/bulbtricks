import time, sched
import threading
import logging
import blessed

class ConsoleDriver:
    def __init__(self, matrix):
        self.frequency = 30
        self.running = False
        self.matrix = matrix
        self.terminal = blessed.Terminal()
        
        self._scheduler_thread = None
    
    def run(self):
        if not self.running:
            scheduler = sched.scheduler(time.time, time.sleep)
            self.running = True
            self.terminal.enter_fullscreen()
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
        self.terminal.exit_fullscreen()
        if self._scheduler_thread:
            self._scheduler_thread.join()
            self._scheduler_thread = None
        
    def render(self):
        self.terminal.clear()
        with self.terminal.location():
            for row in range(self.matrix.rows):
                ypos = 1 + row * 2
                for col in range(self.matrix.columns):
                    xpos = 1 + col * 5
                    b = 0
                    try:
                        b = self.matrix[col][row].brightness
                    except:
                        pass
                    print(term.move(ypos, xpos) + "{0:.1g}".format(b))
        
import time, sched
import threading
import logging
import blessed

ASCIIGREYMAP = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

class ConsoleDriver:
    def __init__(self, matrix):
        self.frequency = 30
        self.running = False
        self.matrix = matrix
        self.terminal = blessed.Terminal()
        self.mode = 'percent'
        
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
        print(self.terminal.clear())
        with self.terminal.location():
            for row in range(self.matrix.rows):
                for col in range(self.matrix.columns):
                    b = 0
                    try:
                        b = self.matrix.at(col,row).brightness * 100
                    except:
                        pass
                    output = "0"
                    if self.mode == 'percent':
                        ypos = 1 + row * 2
                        xpos = 1 + col * 6
                        output = "{0:3.1f}".format(b).rjust(5)
                    if self.mode == 'character':
                        xpos = 1 + row
                        ypos = 1 + col
                        output = ASCIIGREYMAP[max(0, min( int( (1-b)*len(ASCIIGREYMAP) ), len(ASCIIGREYMAP)-1 ))]
                    print(self.terminal.move(ypos, xpos) + output)
        
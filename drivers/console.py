import time, sched
import threading
import logging
import blessed
from drivers.displaydriver import DisplayDriver

ASCIIGREYMAP = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

class ConsoleDriver(DisplayDriver):
    def __init__(self, matrix):
        DisplayDriver.__init__(self, matrix)
        self.terminal = blessed.Terminal()
        self.mode = 'percent'
            
    def on_start(self):
        self.terminal.enter_fullscreen()
        
    def on_stop(self):
        self.terminal.exit_fullscreen()

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
                        ypos = 1 + row
                        xpos = 1 + col
                        output = ASCIIGREYMAP[max(0, min( int( (1-(b/100))*len(ASCIIGREYMAP) ), len(ASCIIGREYMAP)-1 ))]
                    print(self.terminal.move(ypos, xpos) + output)
        
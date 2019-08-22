import time, sched
import threading
import logging

class Matrix:
    def __init__(self, rows, columns):
        self.frequency = 240
        self.running = False
        self._matrix = [ [None for x in range(0, columns)] for y in range(0, rows) ]
        
        self._scheduler_thread = None
        
        
    @property
    def rows(self):
        return len(self._matrix)
        
    @property
    def columns(self):
        return len(next((r for r in self._matrix),''))
        
    @property
    def children(self):
        children = []
        def unpack(m):
            for c in m:
                try:
                    len(c)
                    unpack(c)
                except:
                    children.append(c)
        unpack(self._matrix)
        return children
    
    def run(self):
        if not self.running:
            scheduler = sched.scheduler(time.time, time.sleep)
            self.running = True
            def fn():
                self.tick()
                if self.running:
                    scheduler.enter(1.0 / self.frequency, 0, fn, ())
            def fn_start():
                scheduler.enter(1.0 / self.frequency, 0, fn, ())
                scheduler.run()
            self._scheduler_thread = threading.Thread(target = fn_start)
            self._scheduler_thread.start()
        
    def stop(self):
        self.running = False
        if self._scheduler_thread:
            self._scheduler_thread.join()
            self._scheduler_thread = None
        
    def tick(self):
        for child in self.children:
            if child:
                try:
                    child.tick()
                except:
                    logging.exception('in child {}'.format(child))
                
    def add(self, item, x, y, replace = True):
        if self._matrix[x][y] and not replace:
            raise Exception('Cell already occupied')
        self._matrix[x][y] = item
        
    def at(self, x, y):
        if x < self.rows and y < self.columns:
            return self._matrix[x][y]
        return None
        
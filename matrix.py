import time, sched
import threading
import logging

class Matrix:
    def __init__(self, columns, rows):
        self.frequency = 240
        self.running = False
        self.effects = []
        self._matrix = [ [None for x in range(0, rows)] for y in range(0, columns) ]
        self._scheduler_thread = None
        
        
    @property
    def columns(self):
        return len(self._matrix)
        
    @property
    def rows(self):
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
        return list(set(children))
        
    def add_effect(self, effect):
        if effect not in self.effects:
            wasrunning = False
            if self.running:
                self.stop()
                wasrunning = True
            self.effects.append(effect)
            effect.initialize(self)
            if wasrunning:
                self.run()
        
    def remove_effect(self, effect):
        wasrunning = False
        if self.running:
            self.stop()
            wasrunning = True
        effect.remove()
        self.effects.remove(effect)
        if wasrunning:
            self.run()
    
    def run(self):
        if not self.running:
            scheduler = sched.scheduler(time.time, time.sleep)
            self.running = True
            def fn():
                if self.running:
                    scheduler.enter(1.0 / self.frequency, 0, fn, ())
                self.tick()
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
        completed = []
        for effect in self.effects:
            if effect.completed:
                self.effect.on_completed(self)
                completed.append(effect)
            if effect not in completed:
                effect.tick()
        for effect in completed:
            self.remove_effect(effect)
        for child in self.children:
            if child:
                try:
                    child.tick()
                except:
                    logging.exception('in child {}'.format(child))
                
    def add(self, item, column, row, replace = True):
        if self._matrix[column][row] and not replace:
            raise Exception('Cell already occupied')
        self._matrix[column][row] = item
        
    def at(self, column, row):
        if row < self.rows and column < self.columns:
            return self._matrix[column][row]
        return None
        
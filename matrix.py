import time, sched
import threading
import logging

class Matrix:
    def __init__(self, columns, rows):
        self.frequency = 60
        self.running = False
        self.paused = False
        self.effects = []
        self._matrix = [ [None for x in range(0, rows)] for y in range(0, columns) ]
        self._scheduler_thread = None
        self._speed = 1
        
        
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
            paused = self.paused
            if not paused:
                self.pause()
            self.effects.append(effect)
            effect.initialize(self)
            if not paused:
                self.play()
        
    def remove_effect(self, effect):
        if effect in self.effects:
            paused = self.paused
            if not paused:
                self.pause()
            effect.remove()
            self.effects.remove(effect)
            if not paused:
                self.play()
            
    def remove_all_effects(self):
        for effect in [e for e in self.effects]:
            self.remove_effect(effect)
    
    def run(self):
        if not self.running:
            scheduler = sched.scheduler(time.time, time.sleep)
            self.running = True
            def fn():
                if self.running:
                    scheduler.enter(1.0 / self.frequency / self._speed, 0, fn, ())
                self.tick()
            def fn_start():
                scheduler.enter(1.0 / self.frequency / self._speed, 0, fn, ())
                scheduler.run()
            self._scheduler_thread = threading.Thread(target = fn_start)
            self._scheduler_thread.start()
        
    def stop(self):
        self.running = False
        if self._scheduler_thread:
            self._scheduler_thread.join()
            self._scheduler_thread = None
            
    def pause(self):
        self.paused = True
        
    def play(self):
        self.paused = False
        
    def tick(self):
        if not self.paused:
            completed = []
            for effect in self.effects:
                if effect.completed:
                    completed.append(effect)
            for effect in completed:
                self.remove_effect(effect)
                effect.on_completed()()
            for effect in self.effects:
                effect.tick()
            for child in self.children:
                if child:
                    try:
                        child.tick()
                    except:
                        logging.exception('in child {}'.format(child))
                    
    def replace(self, item, withitem):
        for column in range(self.columns):
            for row in range(self.rows):
                if self._matrix[column][row] == item:
                    self.add(withitem, column, row, replace = True)
                
    def add(self, item, column, row, replace = True, match_freq = True):
        if self._matrix[column][row] and not replace:
            raise Exception('Cell already occupied')
        if match_freq:
            item.frequency = self.frequency
        self._matrix[column][row] = item
        
    def at(self, column, row):
        if row < self.rows and column < self.columns:
            return self._matrix[column][row]
        return None
        
    def brightness_at(self, column, row):
        try:
            return self.at(column, row).brightness
        except:
            pass
        return 0
        
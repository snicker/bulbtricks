import time, sched
import threading
import logging
import requests
from drivers.displaydriver import DisplayDriver

class OLAWebDriver(DisplayDriver):
    def __init__(self, matrix, host = 'localhost', port = 9090, universe = 1):
        DisplayDriver.__init__(self, matrix)
        self.host = host
        self.port = port
        self.universe = universe
        self.channel_map = {}
        
    @property
    def ola_url(self):
        return "http://{host}:{port}/set_dmx".format(host = self.host, port = self.port)

    def render(self):
        channel = 0
        values = {x:0 for x in range(4)}
        for col in range(self.matrix.columns):
            for row in range(self.matrix.rows):
                channel_remap = self.channel_map.get(channel, channel)
                if channel_remap:
                    b = 0
                    try:
                        b = int(self.matrix.at(col,row).brightness * 255)
                    except:
                        pass
                    values[channel_remap] = b
                channel += 1
        out = ','.join([str(values.get(c,0)) for c in range(max(values.keys()) + 1)])
        resp = requests.post(self.ola_url, data = {'u': self.universe, 'd': out})
        if resp:
            if resp.text != 'ok':
                logging.error('bad response from OLA {}'.format(resp.text))
        else:
            logging.error('OLA did not respond in a timely manner')
        
        
        
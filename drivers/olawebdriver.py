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
        self.channel_limit = 512
        
    @property
    def ola_url(self):
        return "http://{host}:{port}/set_dmx".format(host = self.host, port = self.port)

    def render(self):
        def get_values():
            channel = 0
            values = {x:0 for x in range(4)}
            for row in range(self.matrix.rows):
                for col in range(self.matrix.columns):
                    channel_remap = self.channel_map.get(channel, channel)
                    if channel_remap is not None and channel_remap > -1:
                        b = 0
                        try:
                            b = int(self.matrix.at(col,row).brightness * 255)
                        except:
                            pass
                        values[channel_remap] = b
                    channel += 1
                    if channel >= self.channel_limit:
                        return values
            return values
        values = get_values()
        out = ','.join([str(values.get(c,0)) for c in range(max(values.keys()) + 1)])
        logging.debug("sending data to OLA at {}:{}: {}".format(self.host, self.port, out))
        resp = requests.post(self.ola_url, data = {'u': self.universe, 'd': out})
        if resp:
            if resp.text != 'ok':
                logging.error('bad response from OLA {}'.format(resp.text))
        else:
            logging.error('OLA did not respond in a timely manner')
        
        
        
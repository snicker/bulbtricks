import time, sched
import threading
import logging
import requests
from bulbtricks.drivers.displaydriver import DisplayDriver

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
        return "http://{host}:{port}".format(host = self.host, port = self.port)
        
    @property
    def set_dmx_url(self):
        return "{}/set_dmx".format(self.ola_url)
        
    @property
    def universe_plugin_list_url(self):
        return "{}/json/universe_plugin_list".format(self.ola_url)
        
    def get_universes(self):
        universes = []
        try:
            resp = requests.get(self.universe_plugin_list_url)
            if resp:
                jresp = resp.json()
                universes = jresp.get('universes') or []
        except:
            logging.exception('could not fetch universe data from ola')
        return universes
    
    def validate_universe(self, universe):
        universes = self.get_universes()
        if universes:
            for udata in universes:
                if universe == udata.get('id'):
                    return True
        return False

    def run(self):
        if self.validate_universe(self.universe):
            DisplayDriver.run(self)
        else:
            logging.error('Universe ID {} not found on OLA instance'.format(self.universe))

    def render(self):
        def get_values():
            channel = 0
            values = {x:0 for x in range(4)}
            for row in range(self.matrix.rows):
                for col in range(self.matrix.columns):
                    b = 0
                    try:
                        b = int(self.matrix.brightness_at(col,row) * 255)
                    except:
                        pass
                    values[channel] = b
                    channel += 1
                    if channel >= self.channel_limit:
                        return values
            return values
        values = get_values()
        for k in self.channel_map:
            values[self.channel_map[k]] = values[k]
        out = ','.join([str(values.get(c,0)) for c in range(max(values.keys()) + 1)])
        logging.debug("sending data to OLA at {}:{}: {}".format(self.host, self.port, out))
        resp = requests.post(self.set_dmx_url, data = {'u': self.universe, 'd': out})
        if resp:
            if resp.text != 'ok':
                logging.error('bad response from OLA {}'.format(resp.text))
        else:
            logging.error('OLA did not respond in a timely manner')
        
        
        
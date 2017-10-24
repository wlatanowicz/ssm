from elasticsearch_dsl import DocType, Date, Text, Double
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import streaming_bulk
from elasticsearch import Elasticsearch
from datetime import datetime
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

import configparser
import logging
import json

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

config = configparser.ConfigParser()
config.read('/config/server.ini')

logging.debug("Config loaded")

clients = configparser.ConfigParser()
clients.read('/config/clients.ini')

logging.debug("Client list loaded")

es = Elasticsearch([
        config['elasticsearch']['host'] + ':' + config['elasticsearch']['port']
    ])


class Measurement(DocType):
    device_id = Text()
    timestamp = Date()
    s1 = Double()
    s2 = Double()

    class Meta:
        index = 'measurements'

    @classmethod
    def array_factory(cls, input_measurements):
        measurements = []
        for m in input_measurements:
            measurements.append(cls.from_dict(m))
        return measurements

    @classmethod
    def from_dict(cls, m):
        ts = datetime.utcfromtimestamp(float(m['ts']))
        return cls(device_id=m['id'], timestamp=ts, s1=m['s1'], s2=m['s2'])


class MessageReceiver(WebSocket):

    def handleMessage(self):
        logging.debug("Message (%s) from %s", self.data, self.address)
        data = json.loads(self.data)
        if isinstance(data, dict):
            try:
                mes = Measurement.from_dict(data)
                mes.save(es)
            except Exception as e:
                logging.debug("Error storing measurement", e)
        if isinstance(data, list):
            try:
                mes = Measurement.array_factory(data)
                for ok, info in streaming_bulk(es, (d.to_dict(True) for d in mes)):
                    print("Document with id %s indexed." % info['index']['_id'])
            except Exception as e:
                logging.debug("Error storing measurement", e)

    def handleConnected(self):
        logging.debug("Connected %s", self.address)

    def handleClose(self):
        logging.debug("Disconnected %s", self.address)


server = SimpleWebSocketServer(
    config['websocket']['host'],
    int(config['websocket']['port']),
    MessageReceiver
)
server.serveforever()

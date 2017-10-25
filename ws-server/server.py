from elasticsearch_dsl import DocType, Date, Text, Double
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import streaming_bulk
from elasticsearch import Elasticsearch
from datetime import datetime
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

import configparser
import logging
import json

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

config = configparser.ConfigParser()
config.read('/config/server.ini')

logging.debug("Config loaded")

clients = configparser.ConfigParser()
clients.read('/config/clients.ini')
client_list = clients['clients']

logging.debug("Client list loaded")

es = Elasticsearch([
        config['elasticsearch']['host'] + ':' + config['elasticsearch']['port']
    ])


class Measurement(DocType):
    device_id = Text()
    device_name = Text()
    timestamp = Date()
    s = Double()

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
        ts = datetime.now()
        device_name = client_list[m['id']]
        return cls(
            device_id=m['id'],
            device_name=device_name,
            timestamp=ts,
            s=m['s']
        )


class MessageReceiver(WebSocket):

    def handleMessage(self):
        logging.info("Message (%s) from %s", self.data, self.address)
        data = json.loads(self.data)
        if isinstance(data, dict):
            try:
                mes = Measurement.from_dict(data)
                mes.save(es)
            except Exception as e:
                logging.error("Error storing measurement", e)
        if isinstance(data, list):
            try:
                mes = Measurement.array_factory(data)
                for ok, info in streaming_bulk(es, (d.to_dict(True) for d in mes)):
                    print("Document with id %s indexed." % info['index']['_id'])
            except Exception as e:
                logging.error("Error storing measurements", e)

    def handleConnected(self):
        logging.info("Connected %s", self.address)

    def handleClose(self):
        logging.info("Disconnected %s", self.address)


server = SimpleWebSocketServer(
    config['websocket']['host'],
    int(config['websocket']['port']),
    MessageReceiver
)
server.serveforever()

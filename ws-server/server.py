from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text, Double
from elasticsearch_dsl.connections import connections

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

connections.create_connection(
    hosts=[
        config['elasticsearch']['host'] + ':' + config['elasticsearch']['port']
    ]
)


class Measurement(DocType):
    device_id = Text()
    timestamp = Integer()
    s1 = Double()
    s2 = Double()

    class Meta:
        index = 'measurements'


class MessageReceiver(WebSocket):

    def handleMessage(self):
        logging.debug("Message (%s) from %s", self.data, self.address)
        data = json.loads(self.data)
        try:
            mes = Measurement(
                device_id=data['id'],
                timestamp=data['ts'],
                s1=data['s1'],
                s2=data['s2']
            )
            mes.save()
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

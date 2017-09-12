from elasticsearch import Elasticsearch
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import configparser
import logging

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

config = configparser.ConfigParser()
config.read('/config/server.ini')

logging.debug("Config loaded")

clients = configparser.ConfigParser()
clients.read('/config/clients.ini')

logging.debug("Client list loaded")

es = Elasticsearch(config['elasticsearch'])

class MessageReceiver(WebSocket):

    def handleMessage(self):
        logging.debug("Message (%s) from %s", self.data, self.address)
        self.sendMessage(self.data)

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

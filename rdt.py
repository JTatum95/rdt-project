import sys
import threading
import collections
import queue
from network import *
import random

IPPROTO_RDT = 0xfe

class RDTSocket(StreamSocket):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port = None
        self.addr = None
        ports = []
        addrs = []
        # Other initialization here

    def bind(self, port): # Assigns port to socket
        # Check if available
        self.port = port

    def listen(self): # Waits for a connection
        pass

    def accept(self): # Clones socket with open port
        pass

    def connect(self, addr): # Tell a server you want to connect
        if self.port == None:
                self.port = self.random_port() # Bind random
        self.addr = addr

    def send(self, data): # Tell client to recieve from you
        # Check connected
        # Send if able
        self.output(data, self.addr)
            # Wait for ACK

    def input(self, data, src): # Tell proto that someone is connecting
        self.deliver(data, src)

    def sendto(self, msg, dst):
        # Extract header then send
        self.output(msg, dst)

    def random_port():
        num = random.randint(1024, 8000)
        # check if num is taken
        return num

class RDTProtocol(Protocol):
    PROTO_ID = IPPROTO_RDT
    SOCKET_CLS = RDTSocket

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sock = super().socket() 
        # Other initialization here
        # Do multiplexing things

    def socket(self):
        # Check if socket is in use, get unused
        return self.sock

    def input(self, seg, rhost):
        pass
        # self.sock.input(seg, src)

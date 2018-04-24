import sys
import threading
import collections
import queue
from network import *
import random

IPPROTO_RDT = 0xfe

# Global variables
ports = []
addrs = []

class RDTSocket(StreamSocket):
    # Initialize 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port = None
        self.addr = None
        # Other initialization here

    # Assigns port to socket
    def bind(self, port): 
        # Check if available
        if port not in ports:
            self.port = port
            ports.append(port)
        else:
            pass # TODO Random or error

    # Waits for a connection
    def listen(self):
        pass # TODO how do I wait?

    # Clones socket with open port
    def accept(self): 
        sock = super.socket()
        # TODO everything

    # Tell a server you want to connect
    def connect(self, addr): 
        if self.port == None:
                self.port = self.random_port() # Bind random
        self.addr = addr
        addrs.append(addr)
        
    # Tell client to recieve from you
    def send(self, data): 
        # Check connected
        # Send if able
        self.output(data, self.addr)
            # Wait for ACK

    # Tell proto that someone is connecting
    def input(self, data, src):
        self.deliver(data, src)

    # Send to specific client
    def sendto(self, msg, dst):
        # Extract header then send
        self.output(msg, dst)

    # Generate random free port number
    def random_port():
        num = random.randint(1024, 8000)
        while(num in ports):
            num = random.randint(1024, 8000)
        return num

class RDTProtocol(Protocol):
    PROTO_ID = IPPROTO_RDT
    SOCKET_CLS = RDTSocket

    # Initialize
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sock = super().socket() 
        # Other initialization here
        # Do multiplexing things

    # Create new socket
    def socket(self):
        # Check if socket is in use, get unused
        return self.sock

    # TODO idk 
    def input(self, seg, rhost):
        pass
        # self.sock.input(seg, src)

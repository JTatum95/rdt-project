import sys
import threading
import collections
import queue
from network import *
import random

IPPROTO_RDT = 0xfe

class RDTSocket(StreamSocket):

    inque = queue.Queue()

    # Initialize 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port = None
        self.addr = None
        # Other initialization here

    # Clones socket with open port
    def accept(self): 
        inque.put(recv())
        # Strip headers and return

    # Tell a server you want to connect
    # Agree to communicate
    def connect(self, addr): 
        if self.port == None:
                bind(self, self.proto.random_port()) # Bind random ununsed
        self.addr = addr
        output(self, (self, addr), addr) 
        # Connect wait for timeout
 
    # Waits for a connection
    def listen(self):
        if self.port == None:
            raise StreamSocket.NotBound
        if self.addr != None:
            raise StreamSocket.AlreadyConnected
         
    
    # Assigns port to socket
    def bind(self, port): 
        # Check if available
        if self.proto.pairs.get(port) == None:
            raise Socket.AddressInUse
        if self.addr != None: 
            raise StreamSocket.AlreadyConnected
        self.port = port

    # Call deliver when ready to send    
    # Tell client to recieve from you
    def send(self, data): 
        # Check connected
        if self.addr == None:
            raise StreamSocket.NotConnected
        # Send if able
        self.output(data, self.addr)
            # Wait for ACK

    # Tell proto that someone is connecting
    def input(self, data, src):
        self.deliver(data, src)

    def make(self, msg):
        string = self.addr + "," + self.port + "," + msg

# One per host
# Stop and wait
class RDTProtocol(Protocol):
    PROTO_ID = IPPROTO_RDT
    SOCKET_CLS = RDTSocket

    # Keep track of
    # Initialize
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pairs = {} 
        # Other initialization here
        # Do multiplexing things - packet -> socket

    # Create new socket
    def socket(self):
        # Check if socket is in use, get unused
        return self.sock

    def input(self, seg, rhost):
        pass
        # self.sock.input(seg, src)

    # Generate random free port number
    def random_port():
        num = random.randint(30000, 60000)
        while(num in pairs.keys):
            num = random.randint(30000, 60000)
        return num

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
        self.rpair = None
        # self.proto = RDTProtocol(self)
        # Other initialization here

    # Clones socket with open port
    def accept(self): 
     
        # inque.put(recv())
        # Strip headers and return

    # Tell a server you want to connect
    # Agree to communicate
    def connect(self, addr): # IP & Port
        if self.port == None:
            num = self.proto.random_port() 
            self.bind(self, num) # Bind random ununsed
        self.rpair = addr
        self.proto.pairs[self.addr] = self.port 
        # Connect wait for timeout
 
    # Waits for a connection
    def listen(self):
        if self.port == None:
            raise StreamSocket.NotBound
        if self.addr != None:
            raise StreamSocket.AlreadyConnected
        new = inque.get() 

    # Assigns port to socket
    def bind(self, port): 
        # Check if available
        if port in self.proto.ports:
            raise Socket.AddressInUse
        if self.addr != None:
            raise StreamSocket.AlreadyConnected
        self.port = port
        self.proto.ports.append(port)

    # Send to q
    def input(self, data, src):
        inque.put((self.port, self.addr), src)
        # wait for ack
        # timer
        # deliver()

    # Call deliver when ready to send    
    # Tell client to recieve from you
    def send(self, data): 
        # Check connected
        if self.addr == None:
            raise StreamSocket.NotConnected
        # Send if able
        self.output(data, self.addr)
            # Wait for ACK

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
        self.ports = []   
        self.pairs = {} 
        # Other initialization here
        # Do multiplexing things - packet -> socket

    # Create new socket
    # def socket(self):
        # Check if socket is in use, get unused
        # return RDTSocket()

    def input(self, seg, rhost):
    
        # Demux 
        # caddr, cport, msg = seg.split(",",3)
        # self.sock.input(seg, src)

    # Generate random free port number
    def random_port(self):
        num = random.randint(30000, 60000)
        while(num in pairs.keys):
            num = random.randint(30000, 60000)
        return num

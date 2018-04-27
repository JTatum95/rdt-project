import sys
import threading
import collections
import queue
from network import *
import random

IPPROTO_RDT = 0xfe

class RDTSocket(StreamSocket):


    # Initialize 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port = None
        self.rpair = None
        self.server = False
        self.inque = queue.Queue()
        # self.proto = RDTProtocol(self)
        # Other initialization here

    # Clones socket with open port
    def accept(self): 
        if self.server == False:
            raise StreamSocket.NotListening
        new = self.inque.get() 
          
        # inque.put(recv())
        # Strip headers and return

    # Tell a server you want to connect
    # Agree to communicate
    def connect(self, addr): # IP & Port
        if self.port == None:
            num = self.proto.random_port() 
            self.bind(self, num) # Bind random ununsed
        self.rpair = addr
        self.proto.pairs[self.port] = addr 
        msg = "" + addr[0] + addr[1] + self.port
        self.inque.put(msg)
        # Connect wait for timeout
 
    # Waits for a connection
    def listen(self):
        if self.port == None:
            raise StreamSocket.NotBound
        if self.rpair != None:
            raise StreamSocket.AlreadyConnected
        self.server = True 

    # Assigns port to socket
    def bind(self, port): 
        # Check if available
        if port in self.proto.ports:
            raise Socket.AddressInUse
        if self.port != None:
            raise StreamSocket.AlreadyConnected
        self.port = port
        self.proto.ports.append(port)

    # Send to q
    def input(self, seg, host):
        make(self, seg)
        # Parse for content (SYN, ACK)
        # timer
        output(self, seg, host)

    # Call deliver when ready to send    
    # Tell client to recieve from you
    def send(self, data): 
        # Check connected
        if self.rpair == None:
            raise StreamSocket.NotConnected
        # Send if able
        self.output(data, self.rpair)
            # Wait for ACK

    def make(self, msg):
        string = self.rpair[0] + "," + self.rpair[1] + "," + self.port + "," + msg

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
        self.pairs = {} # Map MY port to dest port, addr pair 
        # Other initialization here
        # Do multiplexing things - packet -> socket

    # Create new socket
    # def socket(self):
        # Check if socket is in use, get unused
        # return RDTSocket()

    def input(self, seg, rhost):
        pass 
        # Demux 
        # caddr, cport, msg = seg.split(",",3)
        # self.sock.input(seg, src)

    # Generate random free port number
    def random_port(self):
        num = random.randint(30000, 60000)
        while(num in pairs.keys):
            num = random.randint(30000, 60000)
        return num

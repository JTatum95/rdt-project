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
        self.addr = None
        
        # Other initialization here

    # Assigns port to socket
    def bind(self, port): 
        # Check if available
        if port in ports:
            raise Socket.AddressInUse
        self.port = port
        ports.append(port)

    # Waits for a connection
    def listen(self):
        pass # queue.queue - Blocking queue 

    # Clones socket with open port
    def accept(self): 
        sock = super.socket()

    # Tell a server you want to connect
    # Agree to communicate
    def connect(self, addr): 
        if self.port == None:
                self.port = self.random_port() # Bind random
        self.addr = addr
        addrs.append(addr)
        # Connect wait for timeout
        
    # Tell client to recieve from you
    def send(self, data): 
        # Check connected
        if self.addr == None
            print("error")
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
        num = random.randint(30000, 60000)
        while(num in ports):
            num = random.randint(30000, 60000)
        return num

# One per host
# Stop and wait
class RDTProtocol(Protocol):
    PROTO_ID = IPPROTO_RDT
    SOCKET_CLS = RDTSocket

    # Keep track of
    # Initialize
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sock = super().socket() 
        # Other initialization here
        # Do multiplexing things - packet -> socket

    # Create new socket
    def socket(self):
        # Check if socket is in use, get unused
        return self.sock

    def input(self, seg, rhost):
        pass
        # self.sock.input(seg, src)

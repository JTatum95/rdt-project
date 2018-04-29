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
        self.rpair = None # rpair[0] = IP, rpair[1] = port
        self.seq = 0 
        self.flag = None

        self.bound = False
        self.accepted = False
        self.connected = False
        self.server = False
        
        self.inque = queue.Queue()
        # self.proto = RDTProtocol(self)
        # Other initialization here
    
    def make(self, msg):
        string = str(self.rpair[0]) + "," + str(self.rpair[1]) + "," \
            + str(self.port) + "," + str(self.seq) + "," + msg
        return string.encode()

    # Clones socket with open port
    def accept(self): 
        if self.server == False:
            raise StreamSocket.NotListening
        
        print("\n\n\n QUEUE")
        print(list(self.inque.queue))
        print("\n\n\n")

        new = self.inque.get() 
        assert new != None
        ip = new[0]
        port = new[1]
        
        socket = self.proto.socket()
        port = self.proto.random_port()
        socket.bind(port) 
        socket.rpair = (ip, port)

        self.accepted = True
        socket.accepted = True
        return (self, (ip, port))

    # Tell a server you want to connect
    # Agree to communicate
    def connect(self, addr): # IP & Port
        if self.connected:
            raise StreamSocket.AlreadyConnected
        if not self.bound:
            num = self.proto.random_port() 
            self.bind(num) # Bind random ununsed
        
        self.rpair = addr
         
        # Handshake
        # msg = "" + str(addr[0]) + "," + str(addr[1]) + "," + str(self.port) + "," + "SYN"
        # msg = msg.encode() 
        msg = self.make("SYN")
        print("SYN" + str(msg)) 
        self.connected = True
        self.proto.output(msg, self.rpair[0]) 

        #stuff = self.inque.get()
        

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
        if self.connected or self.accepted:
            raise StreamSocket.AlreadyConnected
        if (port in self.proto.ports) or self.bound:
            raise Socket.AddressInUse
        
        self.port = port
        self.proto.ports.append(port)
        self.proto.pairs[port] = self
        self.bound = True

    # Send to q
    def input(self, seg, host):
        # caddr, cport, msg = seg.split(",",3)
        # is msg == "ACK"
            # output("SYN")
        # timer
        self.proto.output(seg, host)

    # Call deliver when ready to send    
    # Tell client to recieve from you
    def send(self, data): 
        # Check connected
        if not self.connected:
            raise StreamSocket.NotConnected
        # Send if able
        self.proto.output(data, self.rpair)
            # Wait for ACK


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
        self.pairs = {} # Map MY port to MY socket

    # Create new socket
    # def socket(self):
        # Check if socket is in use, get unused
        # return RDTSocket()
    def input(self, seg, host):
        new = seg.decode().split(",", 4) 
        dport = int(new[1])
        
        """
        dip = new[0]
        sport = int(new[2])
        msg = new[3]
      
        print("\nPORTS ")
        print(self.ports)
        print("\nSRC: " + str(dip) + " " + str(sport) + "\nDES: " + str(dport))
        """

        self.pairs[dport].inque.put((host, dport))
        self.pairs[dport].deliver(seg)
        # Demux 
        # self.sock.input(seg, src)

    # Generate random free port number
    def random_port(self):
        num = random.randint(30000, 60000)
        while(num in self.ports):
            num = random.randint(30000, 60000)
        return num

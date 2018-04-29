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

        self.bound = False
        self.accepted = False
        self.connected = False
        self.server = False
        
        self.inque = queue.Queue()
    
    # Helper function to encode data
    def make(self, flag, msg):
        string = str(self.rpair[0]) + "," + str(self.rpair[1]) + "," \
            + str(self.port) + "," + flag + "," + str(self.seq) + "," + msg
        return string.encode()

    # Clones socket with open port
    def accept(self): 
        if self.server == False:
            raise StreamSocket.NotListening
        
        new = self.inque.get() 
        assert new != None
       
        host = new[0]
        fld = new[1].decode().split(",", 5)
        sip = fld[0]
        sport = int(fld[1])
        dport = int(fld[2])
        flag = fld[3]
        seq = int(fld[4])
        msg = fld[5]

        if flag == "SYN":
        # setup new socket
            socket = self.proto.socket()
            port = self.proto.random_port()
            socket.bind(port) 
            socket.rpair = (host, dport)
    

            enchilada = socket.make("SYNACK", "")
            socket.proto.output(enchilada, host)
            socket.accepted = True
            
            ack = socket.inque.get()
            sign = ack[1].decode().split(",", 5)

            if sign[3] == "ACK":
                socket.connected = True
                return (socket, (socket.rpair[0], socket.rpair[1]))

    # Tell a server you want to connect
    # Agree to communicate
    def connect(self, addr): # IP & Port
        if self.connected:
            raise StreamSocket.AlreadyConnected
        if not self.bound:
            num = self.proto.random_port() 
            self.bind(num) # Bind random ununsed

        """
        print("\nADDR[0]")
        print(addr[0])
        print("RPAIR[0]")
        print(self.rpair[0])
        """

        self.rpair = addr
        # Handshake
        msg = self.make("SYN", "")
        # print("SYN" + str(msg)) 
        self.connected = True
        self.proto.output(msg, addr[0]) 

        stuff = self.inque.get()
        thing = stuff[1]
        fld = thing.decode().split(",", 5)
        #print("GIRL NAH")
        if fld[3] == "SYNACK":
            #print("GIRL YOU LOOKING LIKE A SYNACK")
            self.rpair = (self.rpair[0], fld[2])
            self.proto.output(self.make("ACK", ""), self.rpair[0])
    
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
        if (port in self.proto.pairs) or self.bound:
            raise Socket.AddressInUse
        
        self.port = port
        self.proto.ports.append(port)
        self.proto.pairs[port] = self
        self.bound = True

    # Call deliver when ready to send    
    # Tell client to recieve from you
    def send(self, data): 
        # Check connected
        if not self.connected:
            raise StreamSocket.NotConnected
        # Send if able
        self.proto.output(",".join((self.rpair[0], str(self.rpair[1]), \
                str(self.port), "", "0", "")).encode() + data, self.rpair[0])

# Stop and wait
class RDTProtocol(Protocol):
    PROTO_ID = IPPROTO_RDT
    SOCKET_CLS = RDTSocket

    # Initialize
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ports = []   
        self.pairs = {} # Map MY port to MY socket

     
    def input(self, seg, host):
        new = seg.decode().split(",", 5) 
        dport = int(new[1])
       
        """
        print("DPORT")
        print(dport)
        print("HOST")
        print(host)
        print(dport in self.pairs)
        print(self.pairs) 
        """
        
        if new[3] == "SYN" or new[3] == "ACK" or new[3] == "SYNACK":
            self.pairs[dport].inque.put((host, seg))
        else:
            self.pairs[dport].deliver(new[5].encode())

    # Generate random free port number
    def random_port(self):
        num = random.randint(30000, 60000)
        while(num in self.ports):
            num = random.randint(30000, 60000)
        return num

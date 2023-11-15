import socket
import time
from utils import precise_ms_delay, Packet
import pickle
    
relay_host = '127.0.0.1'  # Change to your target host
relay_port = 12345  # Change to your relay port

relay_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

delay_ms = 1

num_packets = 0
while True:
    
    if(num_packets == 1000):break
    
    delx = 2
    dely = 4
    delz = 6
    
    packet = Packet(delx=delx, dely=dely, delz=delz)
    
    serialized_packet = pickle.dumps(packet)
    # data = bytes(data, 'utf-8')  # Encoding the string to bytes using utf-8
    relay_socket.sendto(serialized_packet, (relay_host, relay_port))

    precise_ms_delay(delay_ms)   
    
    num_packets += 1
     
    # time.sleep(0.001) not accurate 
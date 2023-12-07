import socket
import time
from utils import precise_ms_delay, Packet
import pickle
import json
    
relay_host = '127.0.0.1'  # Change to your target host
relay_port = 12345  # Change to your relay port

relay_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

delay_ms = 10

# Sample object to send
data_to_send = {'sequence': 'value'}  # Replace this with the object you want to send

num_packets = 0

while True:
    
    if(num_packets == 1000):break
    
    # Convert the object to a JSON string
    data_to_send['sequence'] = num_packets
    # serialized_packet = json.dumps(data_to_send)
    serialized_packet = f'{num_packets}'

    # data = bytes(data, 'utf-8')  # Encoding the string to bytes using utf-8
    relay_socket.sendto(serialized_packet.encode('utf-8'), (relay_host, relay_port))

    precise_ms_delay(delay_ms)   
    
    num_packets += 1
     
    # time.sleep(0.001) not accurate 
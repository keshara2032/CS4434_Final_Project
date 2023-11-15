import socket
import time
import pickle


# code to control dobot

# Set the source and target UDP ports
relay_host = '127.0.0.1'  # Change to your relay host
relay_port = 54321  # Change to your relay port


relay_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
relay_socket.bind((relay_host, relay_port))


while True:
    data, addr = relay_socket.recvfrom(1024)  # Adjust buffer size as needed
    deserialized_packet = pickle.loads(data)
    
    print(f"Received data from {addr}:")
    for attr, value in vars(deserialized_packet).items():
        print(f"{attr}: {value}")
    
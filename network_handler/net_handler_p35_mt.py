import socket
import random
import argparse
from utils import precise_ms_delay
import pickle
import threading
import queue
import time

parser = argparse.ArgumentParser(description='Network Handler for Manipulation')

# Adding arguments
parser.add_argument('delay', type=int, help='Delay in (ms)')
parser.add_argument('drop', type=int, help='Packet drop/loss (%)')

# Parse the arguments from the command line
args = parser.parse_args()

# Accessing and using the parsed arguments directly
print("Argument 1: {}".format(args.delay))
print("Argument 2: {}".format(args.drop))

delay_ms = args.delay
drop_percent = args.drop / 100

BUFFER_SIZE = 1024

def udp_relay(source_host, source_port, target_host, target_port):
    source_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    source_socket.bind((source_host, source_port))

    num_packets = 1

    buffer = queue.Queue()

    def send_with_delay():
        nonlocal num_packets
        while True:
            if not buffer.empty():
                data, addr = buffer.get()
                
                deserialized_packet = pickle.loads(data)
                print("Received data from {}: ".format(addr))
                for attr, value in vars(deserialized_packet).items():
                    print("{}: {}".format(attr, value))

                # delay imposition
                precise_ms_delay(delay_ms=delay_ms)

                # Simulate dropping packets based on the drop_percentage
                if random.random() < drop_percent:
                    print("Dropped packet from {}".format(addr))
                    continue  # Skip forwarding the packet if it's dropped

                num_packets += 1
                target_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                target_socket.sendto(data, (target_host, target_port))
                target_socket.close()

                print("Number of packets relayed: ", num_packets)

    send_thread = threading.Thread(target=send_with_delay)
    send_thread.start()

    print("Relay initiated!")
    while True:
        data, addr = source_socket.recvfrom(BUFFER_SIZE)
        buffer.put((data, addr))

if __name__ == "__main__":
    # Set the source and target UDP ports
    source_host = '127.0.0.1'  # Change to your source host
    source_port = 12345  # Change to your source port

    target_host = '127.0.0.1'  # Change to your target host
    target_port = 54321  # Change to your target port

    udp_relay(source_host, source_port, target_host, target_port)

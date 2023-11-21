import socket
import random
import argparse
import json
import pickle
import threading
import queue
import time
import logging
from utils import precise_ms_delay

parser = argparse.ArgumentParser(description='Network Handler for Manipulation')

# Adding arguments
parser.add_argument('--config', type=str, default='config.json', help='Path to JSON config file')

# Parse the arguments from the command line
args = parser.parse_args()

# Load configuration from JSON file
with open(args.config, 'r') as config_file:
    config = json.load(config_file)

delay_config = config.get('delay', {})
drop_config = config.get('drop', {})
log_config = config.get('log', {})

delay_type = delay_config.get('type', 'seq')
delay_values = delay_config.get('values', [100])

drop_type = drop_config.get('type', 'rand')
drop_values = drop_config.get('values', [10, 20])

log_enabled = log_config.get('enabled', True)
print_enabled = log_config.get('print_enabled', True)
log_file_name = log_config.get('file_name', 'relay_log.txt')

BUFFER_SIZE = 1024

logging.basicConfig(filename=log_file_name, level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

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
                if print_enabled:
                    print("Received data from {}: ".format(addr))
                    for attr, value in vars(deserialized_packet).items():
                        print("{}: {}".format(attr, value))

                delay_ms = 0
                drop_percent = 0
                # Check if delay type is not "none"
                if delay_type != 'none':
                    # Choose delay based on the specified type
                    if delay_type == 'seq':
                        delay_ms = delay_values[num_packets % len(delay_values)]
                    elif delay_type == 'rand':
                        delay_ms = random.randint(delay_values[0], delay_values[1])
                    else:
                        raise ValueError("Invalid delay type")
                    # delay imposition
                    precise_ms_delay(delay_ms=delay_ms)

                # Check if drop type is not "none"
                if drop_type != 'none':
                    # Choose drop based on the specified type
                    if drop_type == 'rand':
                        drop_percent = random.uniform(drop_values[0], drop_values[1])
                    elif drop_type == 'seq':
                        drop_percent = drop_values[num_packets % len(drop_values)]
                    else:
                        raise ValueError("Invalid drop type")

                    # Simulate dropping packets based on the drop_percentage
                    if random.random() < drop_percent / 100:
                        if log_enabled:
                            logging.info("Dropped packet from {} at {}".format(addr, time.time()))
                        continue  # Skip forwarding the packet if it's dropped

                num_packets += 1
                target_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                target_socket.sendto(data, (target_host, target_port))
                target_socket.close()

                if log_enabled:
                    logging.info("Relayed packet from {} at {}, [delay: {}, drop: {}]".format(addr, time.time(), delay_ms, drop_percent))

                if print_enabled:
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

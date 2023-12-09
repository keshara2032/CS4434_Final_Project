import socket
import time
import json
import pickle
from utils import precise_ms_delay, Packet
import threading

cold_stand_by_on = False
num_packets = 0

def sender_thread():
    global cold_stand_by_on
    relay_host = '127.0.0.1'  # Change to your relay host
    relay_port = 12345  # Change to your relay port
    relay_port_pri = 54321  # Change to your relay port

    relay_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    relay_socket.setblocking(False)  # Set the socket to non-blocking mode

    # Sample object to send
    data_to_send = {'sequence': 'value'}  # Replace this with the object you want to send

    # Send start packet
    start_packet = {'start': True}
    relay_socket.sendto(pickle.dumps(start_packet), (relay_host, relay_port))

    num_packets = 0
    total_packets = 1000  # Set the total number of packets you want to send

    delay_ms = 10

    while num_packets < total_packets:
        # Convert the object to a JSON string
        # data_to_send['sequence'] = num_packets
        # serialized_packet = json.dumps(data_to_send)
        # serialized_packet = f'{num_packets}'
        data_packet = {'data': num_packets}

        # relay_socket.sendto(serialized_packet.encode('utf-8'), (relay_host, relay_port))
        if cold_stand_by_on:
            relay_socket.sendto(pickle.dumps(data_packet), (relay_host, relay_port_pri))
        else:
            relay_socket.sendto(pickle.dumps(data_packet), (relay_host, relay_port))

        precise_ms_delay(delay_ms) 
        num_packets += 1

    # Send stop packet
    stop_packet = {'stop': True}
    relay_socket.sendto(pickle.dumps(stop_packet), (relay_host, relay_port))

    # Close the socket
    relay_socket.close()

def delay_detection_thread():
    global cold_stand_by_on
    relay_host = '127.0.0.1'  # Change to your sender host
    relay_port =  12346       # Change to your sender port

    relay_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    relay_socket.bind((relay_host, relay_port))

    while True:
        try:
            data, addr = relay_socket.recvfrom(1024)  # Non-blocking
            deserialized_packet = pickle.loads(data)

            if 'delay' in deserialized_packet:
                print(">> Delay detected. Adjusting accordingly.")
                print(">> Cold stand by on")
                cold_stand_by_on = True
                num_packets = deserialized_packet['delay']
                # Add your logic to handle the delay
        except socket.error as e:
            if e.errno == 35:  # Resource temporarily unavailable (non-blocking)
                time.sleep(0.01)  # Adjust sleep time as needed
            else:
                raise  # Propagate other errors

# Create and start the threads
sender_thread = threading.Thread(target=sender_thread)
delay_detection_thread = threading.Thread(target=delay_detection_thread)

sender_thread.start()
delay_detection_thread.start()

# Wait for the sender thread to finish
sender_thread.join()

# The delay detection thread is not joined, as it runs indefinitely until manually stopped

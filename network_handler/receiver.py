import socket
import time
import pickle

# Set the source and target UDP ports
relay_host = '127.0.0.1'  # Change to your relay host
relay_port = 54321  # Change to your relay port

sender_host = '127.0.0.1'  # Change to your relay host
sender_port = 12346        # Change to your relay port

relay_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
relay_socket.bind((relay_host, relay_port))

start_received = False
stop_received = False
last_packet_time = time.time()
last_received_data = -1  # Keep track of the last received data value

def check_delay(last_packet_time, last_received_data):
    # Check for delay and send delay packet to sender
    print(f">>> {start_received} - {stop_received} - {(time.time() - last_packet_time)}")
    if start_received and not stop_received and (time.time() - last_packet_time) > 0.05:  # 10ms delay
        delay_packet = {'delay': last_received_data}
        relay_socket.sendto(pickle.dumps(delay_packet), (sender_host, sender_port))
        print("Delay detected. Sending delay packet to sender.")

while True:
    data, addr = relay_socket.recvfrom(1024)  # Adjust buffer size as needed
    deserialized_packet = pickle.loads(data)
    
    if 'start' in deserialized_packet:
        start_received = True
        last_packet_time = time.time()
        print(f"Received start from {addr}:")
        last_received_data = -1  # Reset last_received_data for non-'data' packets
    elif 'stop' in deserialized_packet:
        stop_received = True
        print(f"Received stop from {addr}:")
        last_received_data = 0  # Reset last_received_data for non-'data' packets
    elif 'data' in deserialized_packet:
        if deserialized_packet['data'] > last_received_data:
            check_delay(last_packet_time, last_received_data)
            last_received_data = deserialized_packet['data']
            last_packet_time = time.time()
            print(f"Received data from {addr}: {last_received_data}   {last_packet_time}")
    else:
        # Handle regular data packet
        print(f"Received data from {addr}:")
        for attr, value in vars(deserialized_packet).items():
            print(f"{attr}: {value}")
        
        last_received_data = 0  # Reset last_received_data for non-'data' packets
        last_packet_time = time.time()



# import socket
# import time
# import pickle

# # Set the source and target UDP ports
# relay_host = '127.0.0.1'  # Change to your relay host
# relay_port = 54321  # Change to your relay port


# sender_host = '127.0.0.1'  # Change to your relay host
# sender_port = 12346        # Change to your relay port

# relay_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# relay_socket.bind((relay_host, relay_port))

# start_received = False
# stop_received = False
# last_packet_time = time.time()

# def check_delay(last_packet_time):
#     # Check for delay and send delay packet to sender
#     print(f">>> {start_received} - {stop_received} - {(time.time() - last_packet_time)}")
#     if start_received and not stop_received and (time.time() - last_packet_time) > 0.02:  # 10ms delay
#         delay_packet = {'delay': True}
#         relay_socket.sendto(pickle.dumps(delay_packet), (sender_host, sender_port))
#         print("Delay detected. Sending delay packet to sender.")

# while True:
#     data, addr = relay_socket.recvfrom(1024)  # Adjust buffer size as needed
#     deserialized_packet = pickle.loads(data)
    
#     if 'start' in deserialized_packet:
#         start_received = True
#         last_packet_time = time.time()
#         print(f"Received start from {addr}:")
#     elif 'stop' in deserialized_packet:
#         stop_received = True
#         print(f"Received stop from {addr}:")
#     elif 'data' in deserialized_packet:
#         check_delay(last_packet_time)
#         last_packet_time = time.time()
#         print(f"Received data from {addr}: {deserialized_packet['data']}   {last_packet_time}")
#     else:
#         # Handle regular data packet
#         print(f"Received data from {addr}:")
#         for attr, value in vars(deserialized_packet).items():
#             print(f"{attr}: {value}")
        
#         last_packet_time = time.time()

 
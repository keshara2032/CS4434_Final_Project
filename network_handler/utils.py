import time


# Define a simple class
class Packet:
    sequence_num = 0
    
    def __init__(self, delx,dely,delz):
        
        self.seq_num = Packet.sequence_num
        self.version = 1
        self.delx = delx
        self.dely = dely
        self.delz = delz
        self.origin_time = int(time.time_ns() // 1e6)
        
        Packet.sequence_num += 1
        
        

def precise_ms_delay(delay_ms):
    target_time = time.time() + delay_ms/1e3  # 1ms delay

    while time.time() < target_time:
        pass  # D
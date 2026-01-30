import time

from capture import get_hash
from notify import notify

def monitor(x,y,w,h, interval: int = 3, auto_off: int = 2000):
    start_time = time.time()
    prev_hash = get_hash(x,y,w,h)

    while True:
        time.sleep(interval)
        
        elapsed_time = time.time() - start_time
        if elapsed_time >= auto_off:
            # print(f"Monitoring reached timeout at {time.time()}")
            return "timeout"
        curr_hash = get_hash(x,y,w,h)
        if prev_hash != curr_hash:
            # print("CHANGE DETECTED")
            notify()
            return "change"

        prev_hash = curr_hash


import time

from capture import get_hash
from notify import notify

def monitor(x,y,w,h, app_state_callback = None, interval: int = 3, auto_off: int = 2000):
    start_time = time.time()
    prev_hash = get_hash(x,y,w,h)

    while True:
        time.sleep(interval)
        
        elapsed_time = time.time() - start_time
        if elapsed_time >= auto_off:
            print(f"Monitoring reached timeout at {time.time()}")
            notify(ntype='timeout')
            if app_state_callback:
                app_state_callback()

            return "timeout"

        curr_hash = get_hash(x,y,w,h)
        if prev_hash != curr_hash:
            print("CHANGE DETECTED")
            notify(ntype='change')
            if app_state_callback:
                app_state_callback()

            return "change"

        prev_hash = curr_hash


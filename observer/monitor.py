import time

from observer.capture import get_hash

def monitor(x,y,w,h, state_callback = None, event_callback = None, interval: int = 3, auto_off: int = 2000):
    start_time = time.time()
    prev_hash = get_hash(x,y,w,h)

    while True:
        time.sleep(interval)
        
        elapsed_time = time.time() - start_time
        if elapsed_time >= auto_off:
            print(f"Monitoring reached timeout at {time.time()}")
            if event_callback:
                event_callback('timeout')

            if state_callback:
                state_callback()

            return "timeout"

        curr_hash = get_hash(x,y,w,h)
        if prev_hash != curr_hash:
            print("CHANGE DETECTED")
            if event_callback:
                event_callback('change')

            if state_callback:
                state_callback()
            
            return "change"

        prev_hash = curr_hash


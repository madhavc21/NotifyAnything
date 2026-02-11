from typing import Literal
import os

import win32con
import win32com.client
import win32gui
import win32api
import win32event
import winerror
import ctypes
import sys

from window.overlay import OverlayWindow
from observer.monitor import monitor as monitor_region
from services.tray import start_tray
from services.notify import notify
from services.startup import run_on_startup

import threading
from enum import Enum

HOTKEY_ID = 1

class AppState(Enum):
    # Defining finite states for the app. Enum creates custom keys/types of fixed values. Here it is # fixed enforced states of the app
    # This makes sure spamming and multiple instances are not created
    IDLE = 1
    SELECTING = 2
    MONITORING = 3

state = AppState.IDLE

def register_hotkey():
    # Ctrl + Shift + E
    win32gui.RegisterHotKey(
        None,
        HOTKEY_ID,
        win32con.MOD_CONTROL | win32con.MOD_SHIFT,
        ord('E')
    )

def message_loop():
    try:
        while True:
            success, msg = win32gui.GetMessage(None, 0, 0)
            # GetMessage returns a tuple like:   
                # msg[0]: hwnd (Window handle)
                # msg[1]: message (The ID, e.g., WM_HOTKEY)
                # msg[2]: wParam (Extra data)
                # msg[3]: lParam (Extra data)
                # msg[4]: time
                # msg[5]: pt (Cursor position as a (x, y) tuple)    
            if not success:
                break   

            if msg[1] == win32con.WM_HOTKEY: 
                on_hotkey()

            win32gui.TranslateMessage(msg)
            win32gui.DispatchMessage(msg)

    finally:
        win32gui.UnregisterHotKey(None, HOTKEY_ID)

def get_region(start: tuple, end: tuple):
    """
    Gets the origin nomalized screen relative points of the selected region
    
    :param start: x,y coordinates of the selection start
    :type start: tuple
    :param end: x,y coordinates of the selection end
    :type end: tuple
    """
    x1, y1 = start 
    x2, y2 = end

    # Need to normalize the coordinates relative to screen top-left (0,0). x-axis is top-left -> top-right, y-axis is top-left -> bottom left
    # User may drag in any direction
    # p1, p2 are directional 

    # min as the smaller x value will be nearer to origin, which is the left side of screen
    left = min(x1, x2) 

    # min as the smaller y value will be nearer to origin, which is the top side of screen
    top = min(y1, y2)

    # abs because directional info is not relevant
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    return left, top, width, height

def on_event(event_type: Literal['startup','change','timeout','invalid']):
    """
    Wrap notify function to ensure the event_type is passed in as ntype keyword argument.
    Future safety if notify function signature changes
    """
    notify(ntype=event_type)

def reset_state():
    global state
    state = AppState.IDLE

def on_hotkey():
    global state

    if state != AppState.IDLE:
        return
    
    state = AppState.SELECTING
    overlay = OverlayWindow()
    region, target_hwnd = overlay.create_overlay()

    # region = (None,None) is truthy in python
    if not region or not region[0] or not region[1]:
        on_event('invalid')
        reset_state()
        return

    x,y,w,h = get_region(region[0], region[1])

    if w<5 or h<5: # if w or h is less than 5px, invalid region
        on_event('invalid')
        reset_state()
        return

    state = AppState.MONITORING
    # Threading to ensure starting an observer does not block the entire app
    # Creates the observer in a seperate daemon thread from the main app
    threading.Thread(
        name="Thread-observer#0",
        target=monitor_region,
        kwargs={
            "x":x,
            "y":y,
            "w":w,
            "h":h,
            "target_hwnd": target_hwnd,
            "state_callback":reset_state,
            "event_callback":on_event
        }, 
        daemon=True # daemon type threads exit along with the app. If not the app wont close till the observerThread closes
    ).start()

def main():
    run_on_startup(True)
    ctypes.windll.user32.SetProcessDPIAware() # To prevent DPI scaling, causing mismatch bw mouse coords and screen coords

    on_event("startup")
    mutex = win32event.CreateMutex(
        None,
        False,
        "NotifyAnythingMutex"
    )
    main_tid = win32api.GetCurrentThreadId() # Get the main thread ID
    # We need to run tray in a seperate thread to keep it alive and responsive at all times
    # The main thread is blocked by the message loop, so we need to run the tray in a seperate thread
    # The tray is provided with the main tid, so it can post a quit message to the main thread
    threading.Thread(
        name="Thread-systray",
        target=start_tray,
        args=[main_tid],
        daemon=True
    ).start()

    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        sys.exit(0)
    register_hotkey()
    message_loop()

if __name__ == "__main__":
    main()
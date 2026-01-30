from overlay import select_region
from monitor import monitor_region
import win32con
import win32gui
import win32api

HOTKEY_ID = 1

def register_hotkey():
    # Ctrl + Shift + S
    win32gui.RegisterHotKey(
        None,
        HOTKEY_ID,
        win32con.MOD_CONTROL | win32con.MOD_SHIFT,
        ord('S')
    )

def message_loop():
    try:
        while True:
            success, msg = win32gui.GetMessage(None, 0, 0)
            if not success:
                break   

            if msg.message == win32con.WM_HOTKEY:
                on_hotkey()

            win32gui.TranslateMessage(msg)
            win32gui.DispatchMessage(msg)

    finally:
        win32gui.UnregisterHotKey(None, HOTKEY_ID)

def on_hotkey():
    region = select_region()
    if region:
        monitor_region(region)

def main():
    register_hotkey()
    message_loop()

if __name__ == "__main__":
    main()

import winreg
import sys
import os

REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "NotifyAnything"

def run_on_startup(enabled=True):
    # Get the path to THIS running file (.exe or .py)
    path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
    # We need the absolute path
    exe_path = os.path.abspath(path)
    
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE)
    try:
        if enabled:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
        else:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass
    finally:
        winreg.CloseKey(key)

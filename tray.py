import sys
import win32api
import win32con

from pystray import Icon, Menu, MenuItem
from PIL import Image

def start_tray(main_tid):
    def quit_app(icon, item):
        icon.stop()
        win32api.PostThreadMessage(main_tid, win32con.WM_QUIT, 0, 0)

    icon = Icon(
        "ScreenNotifier",
        Image.new("RGB", (64, 64), "black"),
        menu=Menu(MenuItem("Quit", quit_app))
    )
    icon.run()

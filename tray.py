import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image

def quit_app(icon, item):
    icon.stop()
    sys.exit()

def start_tray():
    icon = Icon(
        "ScreenNotifier",
        Image.new("RGB", (64, 64), "black"),
        menu=Menu(MenuItem("Quit", quit_app))
    )
    icon.run()

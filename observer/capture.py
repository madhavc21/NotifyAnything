import win32gui
import win32ui
import win32con
import win32api
import sys

import hashlib
from pathlib import Path

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
save_path = ASSETS / "capture.bmp"

def capture_selected_bmp(x, y, w, h, save: bool = True, save_name: str = save_path):
    hdc_screen = win32gui.GetDC(0)                      # A DC, Device Context is drawing surface, ie the graphical context you want. In this case we 0 -> desktop window; This returns an HDC (a raw handle) that lets me READ pixels from the screen context.
    hdc_screen_obj = win32ui.CreateDCFromHandle(hdc_screen) # wraps the same raw DC into a python object, enabling function calls on it. hdc_screen is now an reuseable DC object. Creates a Python useable DC obj from raw handle
    bmp = win32ui.CreateBitmap()                        # Creates/initializes an empty bitmap obj, no pixel memory
    bmp.CreateCompatibleBitmap(hdc_screen_obj, w, h)    # Allocates pixel memory ie; properties, h,w,color compatible w screen

    hdc_mem = hdc_screen_obj.CreateCompatibleDC()       # Creates an invisible DC/canvas in memory that follows the same pixel rules as hdc_screen, (ie pixel depth etc.). This is to ensure source and destination are compatible, and pixel conversion is not required when pixel transfer happens. Returns a python DC obj
    hdc_mem.SelectObject(bmp)                           # Attaches the template bmp we created to the mem dc, ie; specifying a place where writes to this dc should go

                                                        # BitBlockTransfer; Transfers pixels from source to destination:
    hdc_mem.BitBlt(                                     # dest.BitBlt(
        (0, 0),                                             # starting from top-left of dest bitmap
        (w, h),                                             # Our selection size w, h
        hdc_screen_obj,                                     # The Source of pixels to transfer; here the screen dc we refered to
        (x, y),                                             # The starting position of our selection in screen
        win32con.SRCCOPY                                    # Copy the pixels exactly
        )                                               # )
    # BitBlt reads pixels from source dc and writes them directly into the destination DC's selcted bitmap
    
    if save:
        bmp.SaveBitmapFile(hdc_mem, str(save_name))          # Saves the bmp at address hdc_mem to a disk address

    hdc_mem.DeleteDC()                                  # IMPORTANT: Delete the mem DC
    hdc_screen_obj.DeleteDC()                           # IMPROTANT: Delete the screen DC wrapper
    win32gui.ReleaseDC(0, hdc_screen)                   # IMPROTANT: Release the raw screen HDC

    return bmp

def get_hash(x,y,w,h):
    bmp = capture_selected_bmp(x,y,w,h, save=False)                 # Don't save files during background monitoring!
    bits = bmp.GetBitmapBits(True) 
    return hashlib.sha256(bits).digest()                # .digest returns a fixed 32 byte hash value, without it we just get a hash object

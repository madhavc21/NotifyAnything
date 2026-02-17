import win32gui
import win32ui
import win32con
from ctypes import windll

import time

import hashlib
from pathlib import Path

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
save_path = ASSETS 


def find_region(xt, yt, target_hwnd):
    """
    Gets the absolute screen coordinates of the selected region
    
    :param xt: x coordinate of the selection start
    :type xt: int
    :param yt: y coordinate of the selection start
    :type yt: int
    :param target_hwnd: handle of the target window
    :type target_hwnd: int
    """
    # xt, yt are stored relative offsets
    # Get current window position
    l, t, r, b = win32gui.GetWindowRect(target_hwnd)
    # The new screen coordinates are (WindowTopLeft + RelativeOffset)
    return l + xt, t + yt

def capture_selected_bmp(xt, yt, w, h, target_hwnd, save: bool = True, save_name: str = save_path):
    # TODO: Adjust the user selected region to fit relative to the target window DC
    # When passing hwnd to GetDC, the returned values are diffrent based on the function
    
    x,y = win32gui.ClientToScreen(target_hwnd, (xt,yt)) 
    # x,y = find_region(xt,yt, target_hwnd) # redundant; ClientToScreen does the same thing
    
    hdc_screen = win32gui.GetWindowDC(target_hwnd)        # A DC, Device Context is drawing surface, ie the graphical context you want. In this case we 0 -> desktop window; This returns an HDC (a raw handle) that lets me READ pixels from the screen context.
    hdc_screen_obj = win32ui.CreateDCFromHandle(hdc_screen) # wraps the same raw DC into a python object, enabling function calls on it. hdc_screen is now an reuseable DC object. Creates a Python useable DC obj from raw handle
    hdc_mem = hdc_screen_obj.CreateCompatibleDC()       # Creates an invisible DC/canvas in memory that follows the same pixel rules as hdc_screen, (ie pixel depth etc.). This is to ensure source and destination are compatible, and pixel conversion is not required when pixel transfer happens. Returns a python DC obj
    
    bmp = win32ui.CreateBitmap()                        # Creates/initializes an empty bitmap obj, no pixel memory
    bmp.CreateCompatibleBitmap(hdc_screen_obj, w, h)    # Allocates pixel memory ie; properties, h,w,color compatible w screen

    hdc_mem.SelectObject(bmp)                           # Attaches the template bmp we created to the mem dc, ie; specifying a place where writes to this dc should go
    
                                                        # BitBlockTransfer; Transfers pixels from source to destination:
    # hdc_mem.BitBlt(                                     # dest.BitBlt(
    #     (0, 0),                                             # starting from top-left of dest bitmap
    #     (w, h),                                             # Our selection size w, h
    #     hdc_screen_obj,                                     # The Source of pixels to transfer; here the screen dc we refered to
    #     (x, y),                                             # The starting position of our selection in screen
    #     win32con.SRCCOPY                                    # Copy the pixels exactly
    #     )                                               # )
    # # BitBlt reads pixels from source dc and writes them directly into the destination DC's selcted bitmap
    # BitBlt only capture the topmost layer, it is difficult to configure for an inactive window
    
    windll.user32.PrintWindow(target_hwnd, hdc_mem.GetSafeHdc(), 2)
    print(f"bmp dims: {bmp.GetInfo()}")
    if save:
        bmp.SaveBitmapFile(hdc_mem, str(save_name))          # Saves the bmp at address hdc_mem to a disk address

    hdc_mem.DeleteDC()                                  # IMPORTANT: Delete the mem DC
    hdc_screen_obj.DeleteDC()                           # IMPROTANT: Delete the screen DC wrapper
    win32gui.ReleaseDC(0, hdc_screen)                   # IMPROTANT: Release the raw screen HDC

    return bmp

def get_hash(x,y,w,h, target_hwnd):
    bmp = capture_selected_bmp(x,y,w,h, target_hwnd, save=True, save_name=f"{save_path}/check_{time.time()}.png")                 # Don't save files during background monitoring!
    bits = bmp.GetBitmapBits(True) 
    return hashlib.sha256(bits).digest()                # .digest returns a fixed 32 byte hash value, without it we just get a hash object

def get_mse(x,y,w,h, target_hwnd):
    bmp = capture_selected_bmp(x,y,w,h, target_hwnd, save=True, save_name=f"{save_path}/check_{time.time()}.png")                 # Don't save files during background monitoring!

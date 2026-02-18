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
    print(f"Selected region relative to target: ({xt}, {yt}, {r-l}, {b-t})")
    # The new screen coordinates are (WindowTopLeft + RelativeOffset)
    return l + xt, t + yt

def create_target_DC(w,h,target_hwnd):

    hdc_screen = win32gui.GetWindowDC(target_hwnd)        # A DC, Device Context is drawing surface, ie the graphical context you want. In this case we 0 -> desktop window; This returns an HDC (a raw handle) that lets me READ pixels from the screen context.
    hdc_screen_obj = win32ui.CreateDCFromHandle(hdc_screen) # wraps the same raw DC into a python object, enabling function calls on it. hdc_screen is now an reuseable DC object. Creates a Python useable DC obj from raw handle
    hdc_mem = hdc_screen_obj.CreateCompatibleDC()       # Creates an invisible DC/canvas in memory that follows the same pixel rules as hdc_screen, (ie pixel depth etc.). This is to ensure source and destination are compatible, and pixel conversion is not required when pixel transfer happens. Returns a python DC obj
    
    bmp = win32ui.CreateBitmap()                        # Creates/initializes an empty bitmap obj, no pixel memory
    bmp.CreateCompatibleBitmap(hdc_screen_obj, w, h)    # Allocates pixel memory ie; properties, h,w,color compatible w screen

    hdc_mem.SelectObject(bmp)    # Attaches the template bmp we created to the mem dc, ie; specifying a place where writes to this dc should go
    return hdc_mem, bmp, hdc_screen_obj, hdc_screen

def create_window_DC(target_hwnd):
    # TODO: Follow DRY principle here
    left, top, right, bot = win32gui.GetClientRect(target_hwnd)
    w = right - left
    h = bot - top
    hdc_screen = win32gui.GetWindowDC(target_hwnd)        # A DC, Device Context is drawing surface, ie the graphical context you want. In this case we 0 -> desktop window; This returns an HDC (a raw handle) that lets me READ pixels from the screen context.
    hdc_screen_obj = win32ui.CreateDCFromHandle(hdc_screen) # wraps the same raw DC into a python object, enabling function calls on it. hdc_screen is now an reuseable DC object. Creates a Python useable DC obj from raw handle
    hdc_mem = hdc_screen_obj.CreateCompatibleDC()       # Creates an invisible DC/canvas in memory that follows the same pixel rules as hdc_screen, (ie pixel depth etc.). This is to ensure source and destination are compatible, and pixel conversion is not required when pixel transfer happens. Returns a python DC obj
    
    bmp = win32ui.CreateBitmap()                        # Creates/initializes an empty bitmap obj, no pixel memory
    bmp.CreateCompatibleBitmap(hdc_screen_obj, w, h)    # Allocates pixel memory ie; properties, h,w,color compatible w screen

    hdc_mem.SelectObject(bmp)  
    return hdc_mem, bmp, hdc_screen_obj, hdc_screen

def capture_selected_bmp(xt, yt, w, h, target_hwnd, save: bool = True, save_name: str = save_path):

    window_hdc, win_bmp, win_scrn_obj, win_hdc_screen = create_window_DC(target_hwnd=target_hwnd)
    region_hdc, region_bmp, rg_scrn_obj, rg_hdc_screen = create_target_DC(w,h,target_hwnd)

    windll.user32.PrintWindow(target_hwnd, window_hdc.GetSafeHdc(), 3)
    
                                                        # BitBlockTransfer; Transfers pixels from source to destination:
    region_hdc.BitBlt(                                     # dest.BitBlt(
        (0, 0),                                             # starting from top-left of dest bitmap
        (w, h),                                             # Our selection size w, h
        window_hdc,                                     # The Source of pixels to transfer; here the screen dc we refered to
        (xt, yt),                                             # The starting position of our selection in screen
        win32con.SRCCOPY                                    # Copy the pixels exactly
        )                                               # )
    # BitBlt reads pixels from source dc and writes them directly into the destination DC's selcted bitmap
    if save:
        region_bmp.SaveBitmapFile(region_hdc, str(save_name))          # Saves the bmp at address hdc_mem to a disk address
    
    # TODO add these in finally block now
    win32gui.DeleteObject(win_bmp.GetHandle())
    window_hdc.DeleteDC()                                  # IMPORTANT: Delete the mem DC
    win_scrn_obj.DeleteDC()                           # IMPROTANT: Delete the screen DC wrapper
    win32gui.ReleaseDC(target_hwnd, win_hdc_screen)                   # IMPROTANT: Release the raw screen HDC
    
    region_hdc.DeleteDC()                                  # IMPORTANT: Delete the mem DC
    rg_scrn_obj.DeleteDC()                           # IMPROTANT: Delete the screen DC wrapper
    win32gui.ReleaseDC(target_hwnd, rg_hdc_screen)                   # IMPROTANT: Release the raw screen HDC

    return region_bmp 

def get_hash(x,y,w,h, target_hwnd):
    bmp = capture_selected_bmp(x,y,w,h, target_hwnd, save=True, save_name=f"{save_path}/check_{time.time()}.png")                 # Don't save files during background monitoring!
    bits = bmp.GetBitmapBits(True) 
    win32gui.DeleteObject(bmp.GetHandle())
    return hashlib.sha256(bits).digest()                # .digest returns a fixed 32 byte hash value, without it we just get a hash object

def get_mse(x,y,w,h, target_hwnd):
    bmp = capture_selected_bmp(x,y,w,h, target_hwnd, save=True, save_name=f"{save_path}/check_{time.time()}.png")                 # Don't save files during background monitoring!

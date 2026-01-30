# main.py
import sys
from overlay import create_overlay
from monitor import monitor
from capture import capture_selected_bmp

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

p1, p2 = create_overlay()

if not p1 or not p2:
    sys.exit(0)

x,y,w,h = get_region(p1,p2)

status = monitor(x,y,w,h)
if status=='change':
    print('change')
    capture_selected_bmp(x,y,w,h)
else:
    print('timeout')


import win32gui, win32api
from pyautogui import position, onScreen
import pyscreeze
import sys
import time

def displayMousePosition(xOffset=0, yOffset=0):
    try:
        runningIDLE = sys.stdin.__module__.startswith("idlelib")
    except:
        runningIDLE = False

    print("Press Ctrl-C to quit.")
    saveText = ""
    lastMouseClick = 0

    if xOffset != 0 or yOffset != 0:
        print("xOffset: %s yOffset: %s" % (xOffset, yOffset))
    try:
        while True:
            # Get and print the mouse coordinates.
            x, y = position()
            positionStr = "X: " + str(x - xOffset).rjust(4) + " Y: " + str(y - yOffset).rjust(4)
            if not onScreen(x - xOffset, y - yOffset) or sys.platform == "darwin":
                # Pixel color can only be found for the primary monitor, and also not on mac due to the screenshot having the mouse cursor in the way.
                pixelColor = ("NaN", "NaN", "NaN")
            else:
                pixelColor = pyscreeze.screenshot().getpixel(
                    (x, y)
                )  # NOTE: On Windows & Linux, getpixel() returns a 3-integer tuple, but on macOS it returns a 4-integer tuple.
            positionStr += " RGB: (" + str(pixelColor[0]).rjust(3)
            positionStr += ", " + str(pixelColor[1]).rjust(3)
            positionStr += ", " + str(pixelColor[2]).rjust(3) + ")"

            # Get mouse window form hwan
            hw = win32gui.WindowFromPoint((x, y))
            positionWindowInfo = " WindowInfo: {Class: "
            positionWindowInfo += win32gui.GetClassName(hw)
            positionWindowInfo += ", Text: "
            positionWindowInfo += win32gui.GetWindowText(hw)
            positionWindowInfo += ", WindowRect: "
            positionWindowInfo += str(win32gui.GetWindowRect(hw))
            positionWindowInfo += "}"
            sys.stdout.write(positionStr + positionWindowInfo)

            if not runningIDLE:
                # If this is a terminal, than we can erase the text by printing \b backspaces.
                sys.stdout.write("\b" * len(positionStr + positionWindowInfo))
            else:
                # If this isn't a terminal (i.e. IDLE) then we can only append more text. Print a newline instead and pause a second (so we don't send too much output).
                sys.stdout.write("\n")
                time.sleep(1)
            sys.stdout.flush()

            mouseClick = win32api.GetKeyState(0x01)
            if mouseClick not in [0, 1] and lastMouseClick in [0, 1]:
                saveText = positionStr + positionWindowInfo
            if saveText != "":
                print("Click: ")
                saveText = ""
                time.sleep(0.1)
            lastMouseClick = mouseClick

    except KeyboardInterrupt:
        sys.stdout.write("\n")
        sys.stdout.flush()

displayMousePosition()
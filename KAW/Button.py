import win32gui, win32ui, win32con, win32api

#For moving the mouse and clicking.
def left(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def right(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)

def ViewEpicBattle():
    left(1774, 314)

def Attack():
    left(1151, 312)

def Fight():
    left(1200, 385)

def Assassinate():
    left(1169, 678)

def ContinueAll():
    left(1130, 811)

def RepeatAction():
    left(985, 678)

def CloseAttackFightAndAsssassinate():
    left(974, 841)

def CloseNoMoreTroops():
    left(970, 605)



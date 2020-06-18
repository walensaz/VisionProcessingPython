import win32gui, win32ui, win32con, win32api, win32com.client

def click(x,y,left):
    if left:
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    else:
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)


def getFireFox():
    top_list, win_list = [], []

    def enum_cb(hwnd, results):
        win_list.append((hwnd, win32gui.GetWindowText(hwnd)))

    win32gui.EnumWindows(enum_cb, top_list)
    firefox = [(hwnd, title) for hwnd, title in win_list if 'firefox' in title.lower()]
    firefox = firefox[0]
    hwin = firefox[0]
    return hwin

def getMinecraft():
    top_list, win_list = [], []

    def enum_cb(hwnd, results):
        win_list.append((hwnd, win32gui.GetWindowText(hwnd)))

    win32gui.EnumWindows(enum_cb, top_list)
    firefox = [(hwnd, title) for hwnd, title in win_list if 'minecraft' in title.lower()]
    firefox = firefox[0]
    hwin = firefox[0]
    return hwin


def convertPixels(img, threshold, switched):
    for x in range(len(img)):
        for y in range(len(img[x])):
            if img[x][y] > threshold:
                img[x][y] = switched
    return img

def convertPixelsOpposite(img, threshold, switched):
    for x in range(len(img)):
        for y in range(len(img[x])):
            if img[x][y] < threshold:
                img[x][y] = switched
    return img

def findPixels(img, pixel, differential):
    for x in range(len(img)):
        for y in range(len(img[x])):
            if img.getPixel(x,y) < pixel + differential:
                img[x][y] = 0
    return img

import numpy as np
import cv2
import win32gui, win32ui, win32con, win32api, win32com.client
import KAW.Utils as Utils
import time


middle_of_window = 450

#In BGR so opposite of RGB
echest_1 = np.asarray([7, 75, 75])  # white!
echest_2 = np.asarray([40, 255, 255])  # yellow! note the order

def right(x, y):
    win32api.SetCursorPos((x, y))
    time.sleep(.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)

def draw_contours(img):
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #print(img[30][40])
        #mask can be showed to check seperate colors
        mask = cv2.inRange(img, echest_1, echest_2)
        ret, thresh = cv2.threshold(mask, 50, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        height, width, _ = img.shape
        min_x, min_y = width, height
        max_x = max_y = 0

        #Used for finding out how the contours look without the if
        #cv2.drawContours(img, contours, -1, (255,255,0),3)


        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if (w > 15 and w < 45) and (h > 50 and h < 100):
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 3)
        return img
    except TypeError:
        return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def custom_get_positions(region=None):
    hwin = Utils.getMinecraft()
    if region:
        left, top, x2, y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())
    return img

def get_enderchest(img):
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img, echest_1, echest_2)
        ret, thresh = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        newcontour = contours[0]
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            if (w > 15 and w < 45) and (h > 50 and h < 100) and (x < 540 and x > 400):
                newcontour = contour
        x, y, w, h = cv2.boundingRect(newcontour)
        return x + (w * .5)
    except IndexError:
        print("cant find!!!")
        return -1

def main():
    time.sleep(2)
    while True:
        img = custom_get_positions(region=(500, 200, 1400, 1000))
        newimg = draw_contours(img)
        x = get_enderchest(img)
        multiplier = 1
        if(x < 540 and x > 390):
            if(x < 460 and x > 440):
                right(772, 428)
            # else:
            #     if(x < 450):
            #         multiplier = -1
            #     click1 = int(((middle_of_window - x) * multiplier) * 2.5)
            #     click = 772 + click1
            #     right(click, 428)
            #     print("click: " + str(click) + " click1: " + str(click1))
            #     time.sleep(2)
        newimg = cv2.resize(newimg, (1600, 780))
        cv2.imshow('window', newimg)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()
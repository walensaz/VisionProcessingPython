import numpy as np
import cv2
import time
import win32gui, win32ui, win32con, win32api, win32com.client
import pytesseract as tes
import KAW.Utils as Utils
import KAW.Button as Button
from pyautogui import press, typewrite, hotkey
from Scratch.keypress import PressKey, ReleaseKey

player_1 = np.asarray([0, 130, 90])  # white!
player_2 = np.asarray([0, 255, 255])  # yellow! note the order

ball_1 = np.asarray([50, 170, 0])  # white!
ball_2 = np.asarray([255, 255, 255])  # yellow! note the order

RIGHT = 0x27
LEFT = 0x25
SPACE = 0x20
A = 0x41
D = 0x44


def draw_contours(img):
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # print(img[30][40])
        mask = cv2.inRange(img, ball_1, ball_2)
        ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        mask = cv2.inRange(img, player_1, player_2)
        ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        contours1, hierarchy1 = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        height, width, _ = img.shape
        min_x, min_y = width, height
        max_x = max_y = 0
        for contour, hier in zip(contours, hierarchy):
            (x, y, w, h) = cv2.boundingRect(contour)
            min_x, max_x = min(x, min_x), max(x + w, max_x)
            min_y, max_y = min(y, min_y), max(y + h, max_y)
            if w > 80 and h > 80:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 3)
        if max_x - min_x > 0 and max_y - min_y > 0:
            cv2.rectangle(img, (min_x, min_y), (max_x, max_y), (255, 255, 0), 2)

        height, width, _ = img.shape
        min_x, min_y = width, height
        max_x = max_y = 0
        for contour, hier in zip(contours1, hierarchy1):
            (x, y, w, h) = cv2.boundingRect(contour)
            min_x, max_x = min(x, min_x), max(x + w, max_x)
            min_y, max_y = min(y, min_y), max(y + h, max_y)
            if w > 80 and h > 80:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 3)
        if max_x - min_x > 0 and max_y - min_y > 0:
            cv2.rectangle(img, (min_x, min_y), (max_x, max_y), (255, 255, 0), 2)
        # img = cv2.drawContours(img, contours, -1, (255, 255, 255), 10)
        return img
    except TypeError:
        return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def custom_get_positions(region=None):
    hwin = Utils.getFireFox()
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


def get_player_pos_x(img):
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img, player_1, player_2)
        ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        x, y, w, h = cv2.boundingRect(contours[0])
        return x + (w * .5)
    except IndexError:
        print("cant find!!!")
        return 500


def get_ball_pos_x(img):
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(img, ball_1, ball_2)
        ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        x, y, w, h = cv2.boundingRect(contours[0])
        return x + (w * .5)
    except IndexError:
        print("cant find!!!")
        return 500


def process_img(image):
    original_image = image
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection
    # processed_img = cv2.Canny(image, threshold1=100, threshold2=500)
    # processed_img = image
    return processed_img


def getColumn(image):
    black_pixels_mask = np.all(image == [0, 0, 0], axis=-1)


def releaseKeys():
    ReleaseKey(SPACE)
    ReleaseKey(LEFT)
    ReleaseKey(RIGHT)


def main():
    keypressed = SPACE
    timesin = 0
    while True:
        # screen = grab_screen(region=(20, 40, 1900, 900))
        # ns = cv2.rectangle(screen, (170, 182), (123, 200), (0, 0, 255), 2)
        # img = cv2.cvtColor(ns, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('window', img)
        current_window = win32gui.GetForegroundWindow()
        start = time.time()
        img = custom_get_positions(region=(383, 157, 1530, 1025))
        if (current_window == Utils.getFireFox()):
            ball_x = get_ball_pos_x(img)
            player_x = get_player_pos_x(img)
            newimg = draw_contours(img)
            newimg = cv2.resize(newimg, (1300, 700))
            cv2.imshow('window', newimg)
            if (ball_x + 28 > player_x and ball_x - 28 < player_x):
                PressKey(SPACE)
            else:
                if (player_x > ball_x):
                    PressKey(LEFT)
                    PressKey(SPACE)
                elif (player_x < ball_x):
                    PressKey(RIGHT)
                    PressKey(SPACE)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
    time.sleep(12)


main()

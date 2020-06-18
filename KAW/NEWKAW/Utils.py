import numpy as np
import cv2
import time
import win32gui, win32ui, win32con, win32api, win32com.client
import pytesseract as tes
import KAW.Utils as Utils
import KAW.Button as Button
from pyautogui import press, typewrite, hotkey
from Scratch.keypress import PressKey, ReleaseKey


def draw_custom_contours(color_1, color_2, img):
    try:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # print(img[30][40])
        mask = cv2.inRange(img, color_1, color_2)
        ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        #contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #img = cv2.drawContours(img, contours, -1, (255, 255, 255), 3)
        return thresh
    except TypeError:
        return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

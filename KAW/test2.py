import numpy as np
import cv2
import time
import win32gui, win32ui, win32con, win32api
import pytesseract as tes
import KAW.Utils as Utils


def grab_screen(region=None):
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

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)


def process_img(image):
    original_image = image
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection
    #processed_img = cv2.Canny(image, threshold1=100, threshold2=500)
    #processed_img = image
    return processed_img

def shouldAttack():
    troop_count_max = tes.image_to_string(process_img(grab_screen(region=(144, 220, 185, 238))))
    current_troop_count = tes.image_to_string(process_img(grab_screen(region=(100, 220, 138, 238))))
    print("Max troop count: " + troop_count_max)
    print("Current troop count " + current_troop_count)
    if (int(troop_count_max) >= int(current_troop_count)):
        return True

def convertPixels(img, threshold, switched):
    for x in range(len(img)):
        for y in range(len(img[x])):
            if(img[x][y] > threshold):
                img[x][y] = switched
    return img


def getClan():
    clan = tes.image_to_string(convertPixels(np.invert(process_img(grab_screen(region=(170, 590, 245, 615)))), 90, 200))
    return clan

def main():
    last_time = time.time()
    while True:
        #screen = grab_screen(region=(20, 40, 1900, 900))
        img = process_img(grab_screen(region=(170, 590, 245, 615)))
        #ns = cv2.line(screen, (1100, 280), (1175, 280), (245,0,0), 5)
        #img = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        #print(tes.image_to_string(process_img(grab_screen(region=(820, 290, 1100, 335)))))
        cv2.imshow('window', Utils.convertPixelsOpposite(
            Utils.convertPixelsOpposite(
                process_img(grab_screen(region=(1695, 305, 1813, 326))), 180, 255), 180, 0))
        cv2.imshow('window2', np.invert(Utils.convertPixelsOpposite(process_img(grab_screen(region=(1695, 305, 1813, 326))), 240, 0)))
        print("spy: " + tes.image_to_string(Utils.convertPixels(np.invert(process_img(grab_screen(region=(1695, 305, 1813, 326)))), 140, 252)))
        #ns = np.asarray(img)
        print('Clan: ' + getClan())
        #if(shouldAttack()):
            #print("Attacking")
            #shell = win32com.client.Dispatch("WScript.Shell")
            #shell.SendKeys('%')
            #win32gui.SetForegroundWindow(utils.getFireFox())
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        #time.sleep(25)
main()

import numpy as np
import cv2
import time
import win32gui, win32ui, win32con, win32api, win32com.client
import pytesseract as tes
import KAW.Utils as Utils
import KAW.Button as Button


# For grabbing the screen of the firefox window, cannot be minimized
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


# Converts the image to gray scale
def process_img(image):
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return processed_img




# Checks how many troops you have, and compares it to how many you should have to attack.
def shouldAttack():
    troop_count_max = tes.image_to_string(process_img(grab_screen(region=(144, 220, 184, 237))))
    current_troop_count = tes.image_to_string(process_img(grab_screen(region=(100, 220, 138, 238))))
    spy_count_max = tes.image_to_string(
        Utils.convertPixels(process_img(grab_screen(region=(145, 272, 192, 293))), 100, 255))
    spy_current_troop = tes.image_to_string(
        Utils.convertPixels(process_img(grab_screen(region=(90, 272, 139, 293))), 100, 255))
    print("Current troop count: " + current_troop_count)
    print("Current Spy count: " + spy_current_troop)
    try:
        if ('(' not in current_troop_count or '(' not in troop_count_max) and int(76200) <= int(current_troop_count):
            return True
    except ValueError:
        print('Troop count messed up!')

    try:
        spy = int(spy_current_troop)
        if '(' not in spy_current_troop and ((spy >= 730000) and (spy <= 800000)):
            return True
    except ValueError:
        print('Assassin count messed up!')
    return False



# Gets the clan and returns it as a string.
def getClan():
    clan = tes.image_to_string(Utils.convertPixels(np.invert(process_img(grab_screen(region=(170, 590, 245, 615)))), 90, 200))
    return clan


def isSuccessfulAttack():
    time.sleep(0.01)
    success = tes.image_to_string(process_img(grab_screen(region=(820, 290, 1100, 335))))
    print('Attack Success: ' + success)
    if('IC' in success or 'gf' in success or len(success) <= 2):
        return True
    else:
        return False


def isOutOfTroops():
    troops = tes.image_to_string(process_img(grab_screen(region=(880, 550, 1035, 575))))
    if 'units' in troops:
        return True
    else:
        return False


def willNotAffect():
    effects = tes.image_to_string(process_img(grab_screen(region=(880, 550, 1035, 575))))
    if 'no effect' in effects:
        return True
    else:
        return False


def hasEb():
    checkeb = tes.image_to_string(np.invert(Utils.convertPixelsOpposite(process_img(grab_screen(region=(1695, 305, 1813, 326))), 240, 0)))
    if 'view' in checkeb:
        print("Eb currently available!")
        return True
    else:
        print("Eb not currently available")
        return False

def Attack():
    time.sleep(1)
    Button.ViewEpicBattle()
    time.sleep(1)
    Button.Attack()
    time.sleep(1)
    Button.Fight()
    time.sleep(1)
    Button.ContinueAll()
    time.sleep(1)
    if not willNotAffect():
        while(isSuccessfulAttack()):
            Button.RepeatAction()
            time.sleep(.1)
            if(willNotAffect()):
                time.sleep(.3)
                Button.CloseNoMoreTroops()
                print('Will not effect!')
                break
            elif(isOutOfTroops()):
                time.sleep(.3)
                print('Out of troops!')
                Button.CloseNoMoreTroops()
                break
            if not isSuccessfulAttack():
                time.sleep(.3)
                Button.CloseAttackFightAndAsssassinate()
                Button.CloseNoMoreTroops()
                print('Not successfull attack!')
                break
            time.sleep(0.001)
    time.sleep(1)
    Button.Attack()
    time.sleep(1)
    Button.Assassinate()
    time.sleep(1)
    Button.ContinueAll()
    time.sleep(1)
    if not willNotAffect():
        while(isSuccessfulAttack()):
            Button.RepeatAction()
            time.sleep(.1)
            if(willNotAffect()):
                time.sleep(.5)
                Button.CloseNoMoreTroops()
                print('Will not effect!')
                break
            elif(isOutOfTroops()):
                time.sleep(.5)
                print('Out of troops!')
                Button.CloseNoMoreTroops()
                break
            if not isSuccessfulAttack():
                time.sleep(.5)
                Button.CloseAttackFightAndAsssassinate()
                Button.CloseNoMoreTroops()
                print('Not successfull attack!')
                break



def main():
    attacks = 0
    while True:
        #screen = grab_screen(region=(20, 40, 1900, 900))
        #ns = cv2.rectangle(screen, (170, 182), (123, 200), (0, 0, 255), 2)
        #img = cv2.cvtColor(ns, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('window', img)
        print("Clan: " + getClan())
        if(len(getClan()) > 2 and 'No clan' not in getClan()):
            if(hasEb()):
                if (shouldAttack()):
                    print("Attacking")
                    current_window = win32gui.GetForegroundWindow()
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shell.SendKeys('%')
                    win32gui.SetForegroundWindow(Utils.getFireFox())
                    Attack()
                    attacks += 1
                    shell.SendKeys('%')
                    win32gui.SetForegroundWindow(current_window)
                    print('times attacked: ' + str(attacks))
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
        time.sleep(50)
    print('times attacked: ' + str(attacks))
main()

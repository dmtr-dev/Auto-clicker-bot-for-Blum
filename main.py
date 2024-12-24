from pynput.mouse import Button, Controller
from termcolor import cprint
from ctypes import windll
from loguru import logger
import pygetwindow as gw
from sys import stderr
import pyautogui
import keyboard
import random
import time


mouse_controller = Controller()

# def pixel_condition(r, g, b):
#     return ((r in range(220, 230) and g in range(115, 130) and b in range(45, 55)) or        # color Pumpkin
#             (r in range(125, 131) and g in range(215, 222) and b in range(229, 233)) or      # color Freezing
#             (r in range(134, 141) and g in range(126, 132) and b in range(126, 132)) or      # color Bomb
#             (r in range(178, 206) and g in range(178, 206) and b in range(178, 206)))        # color Bomb 2

def pixel_condition(r, g, b):
    return ((r in range(90, 110) and g in range(125, 150) and b in range(85, 95)) or        #tree
            (r in range(200, 255) and g in range(35, 65) and b in range(180, 205)) or       #boot
            (r in range(50, 105) and g in range(110, 175) and b in range(5, 40)) or         #ball
            (r in range(185, 255) and g in range(0, 2) and b in range(155, 200)) or         #wand
            (r in range(90, 130) and g in range(165, 210) and b in range(20, 85)) or        #berries
            (r in range(130, 180) and g in range(55, 75) and b in range(5, 20)) or          #gingerbread
            (r in range(190, 240) and g in range(10, 35) and b in range(100, 175)) or       #head
            (r in range(235, 255) and g in range(150, 185) and b in range(0, 15)) or        #candle
            (r in range(85, 105) and g in range(135, 175) and b in range(15, 55)))          #decoration

windll.kernel32.SetConsoleTitleW('Auto clicker bot for Blum | by https://t.me/dmtrcrypto')
cprint("\nTG Channel - https://t.me/dmtrcrypto\n\n", 'magenta')

logger.remove()
logger.add(stderr, format='<cyan>{time:HH:mm:ss}</cyan> | <level>{level:<8}</level> | <cyan><bold>{line}</bold></cyan> | <magenta>Message:</magenta> <level><underline>{message}</underline></level>')

def click(x, y):
    mouse_controller.position = (x, y)
    mouse_controller.press(Button.left)
    mouse_controller.release(Button.left)

input_window_name = input('\nEnter the name of the window with Blum game enabled (Y/y - TelegramDesktop): ')
input_button = input("Do you want the bot to play continuously without your participation until you run out of tickets (y/n): ")

window_name = "TelegramDesktop" if input_window_name.lower() == 'y' else input_window_name

check_window = gw.getWindowsWithTitle(window_name)
if not check_window:
    logger.warning(f'Window "{window_name}" not found.')
else:
    telegram_window = check_window[0]
    logger.success(f'Window "{window_name}" found successfully.')
    print("\n")
    logger.info("Use 'q' to pause or resume.")

paused = True
logger.info('Mode: Stopped')

last_check_time = time.time()

while True:
    if keyboard.is_pressed('q'):
        paused = not paused
        logger.info('Mode: ' + ('Stopped' if paused else 'Working'))
        time.sleep(0.25)

    if paused:
        continue

    if not telegram_window or not telegram_window.visible:
        logger.error(f'Window - "{window_name}" is closed or not found.')
        input("Press Enter to exit...")
        break
    
    win_rect  = (telegram_window.left + 12, telegram_window.top + 140, telegram_window.width - 24, telegram_window.height - 200)

    try:
        telegram_window.activate()
    except:
        telegram_window.minimize()
        telegram_window.restore()

    screenshot = pyautogui.screenshot(region=win_rect)
    width, height = screenshot.size

    for x in range(0, width, 20): # parameters for slowing down the bot
        for y in range(0, height, 20): # parameters for slowing down the bot
            r, g, b = screenshot.getpixel((x, y))
            if pixel_condition(r, g, b):
                click_x = win_rect[0] + x
                click_y = win_rect[1] + y
                click(click_x + random.uniform(1, 2), click_y + random.uniform(1, 2))
                time.sleep(0.01)
                break

    if time.time() - last_check_time > 8 and input_button.lower() == 'y':
        last_check_time = time.time()
        click(win_rect[0] + random.randint(398, 402), win_rect[1] + random.randint(498, 502))
        click(win_rect[0] + random.randint(348, 352), win_rect[1] + random.randint(608, 612))
        time.sleep(0.1)


input("Press Enter to Exit...")

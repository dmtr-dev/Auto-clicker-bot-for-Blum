from pynput.mouse import Button, Controller
from ctypes import windll
from loguru import logger
from sys import stderr
import pyautogui as pag
import pygetwindow as gw
import keyboard
import random
import time

mouse_controller = Controller()

pixel_condition = lambda r, g, b: (r in range(105, 200)) and (g in range(200, 255)) and (b in range(0, 120))

windll.kernel32.SetConsoleTitleW('Auto clicker bot for Blum | by https://t.me/dmtrcrypto')

logger.remove()
logger.add(stderr, format='<cyan>{time:HH:mm:ss}</cyan> | <level>{level:<8}</level> | <cyan><bold>{line}</bold></cyan> | <magenta>Message:</magenta> <level><underline>{message}</underline></level>')

print("\n\n\033[94mTG Channel Creator - https://t.me/dmtrcrypto\033[0m\n")

def click(x, y):
    mouse_controller.position = (x, y + random.randint(1, 3))
    mouse_controller.press(Button.left)
    mouse_controller.release(Button.left)

input_window_name = input('\nEnter the name of the window with Blum game enabled (Y/y - TelegramDesktop): ')
print("\n")

if input_window_name.lower() == 'y':
    window_name = "TelegramDesktop"
else:
    window_name = input_window_name


check_window = gw.getWindowsWithTitle(window_name)
if not check_window:
    logger.warning(f'The window "{window_name}" was not found')
else:
    logger.success(f'The window "{window_name}" was found successfully')
    print("\n")
    logger.info("Use the 'q' button to pause")

telegram_window = check_window[0] if check_window else None
paused = False

while True:
    if keyboard.is_pressed('q'):
        paused = not paused
        if paused:
            logger.info('Mode - Stopped')
        else:
            logger.info('Mode - Work')
        time.sleep(0.25)

    if paused:
        continue

    if not telegram_window or not telegram_window.visible:
        logger.error(f'Window - "{window_name}" closed or not found')
        logger.error("Press Enter to Exit...")
        input()
        break

    win_rect  = (telegram_window.left, telegram_window.top, telegram_window.width, telegram_window.height)

    try:
        telegram_window.activate()
    except:
        telegram_window.minimize()
        telegram_window.restore()

    screenshot = pag.screenshot(region=win_rect)
    width, height = screenshot.size

    pixel_detected = False

    for x in range(0, width, 20):
        for y in range(0, height, 20):
            r, g, b = screenshot.getpixel((x, y))
            if pixel_condition(r, g, b):
                click_x = win_rect[0] + x
                click_y  = win_rect[1] + y
                click(click_x + 4, click_y)
                time.sleep(0.01)
                pixel_found = True
                break
        if pixel_detected:
            break

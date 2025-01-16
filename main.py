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

def pixel_condition(r, g, b):
    return ((r in range(58, 132) and g in range(218, 255) and b in range(0, 43)))

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
last_auto_click_time = time.time()
auto_click_interval = 20 * 60

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

    for x in range(0, width, 35): # parameters for slowing down the bot
        for y in range(0, height, 35): # parameters for slowing down the bot
            r, g, b = screenshot.getpixel((x, y))
            if pixel_condition(r, g, b):
                click_x = win_rect[0] + x
                click_y = win_rect[1] + y
                click(click_x + random.uniform(1, 2), click_y + random.uniform(1, 2))
                time.sleep(0.02)
                break

    # if time.time() - last_auto_click_time >= auto_click_interval:
    #     logger.info("20 minutes passed. Performing automatic click...")
    #     click(win_rect[0] + 370, win_rect[1] - 60)
    #     last_auto_click_time = time.time()
    #     time.sleep(1)
    #     click(win_rect[0] + 360, win_rect[1] - 60)

    if time.time() - last_check_time > 8 and input_button.lower() == 'y':
        last_check_time = time.time()
        click(win_rect[0] + 350, win_rect[1] + 608)
        time.sleep(0.1)


input("Press Enter to Exit...")

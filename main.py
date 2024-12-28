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
    return ((r in range(200, 255) and g in range(34, 65) and b in range(184, 200)) or         # candy
            (r in range(87, 129) and g in range(160, 203) and b in range(23, 60)) or          # berries
            (r in range(209, 239) and g in range(0, 14) and b in range(149, 167)) or          # head
            (r in range(234, 234) and g in range(250, 251) and b in range(120, 122)) or       # head
            (r in range(132, 180) and g in range(56, 88) and b in range(7, 38)) or            # gingerbread
            (r in range(43, 58) and g in range(88, 111) and b in range(24, 36)) or            # tree
            (r in range(176, 183) and g in range(236, 242) and b in range(250, 255)) or       # candle
            (r in range(196, 255) and g in range(15, 32) and b in range(172, 195)))           # boots


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

    for x in range(0, width, 25): # parameters for slowing down the bot
        for y in range(0, height, 25): # parameters for slowing down the bot
            r, g, b = screenshot.getpixel((x, y))
            if pixel_condition(r, g, b):
                click_x = win_rect[0] + x
                click_y = win_rect[1] + y
                click(click_x + random.uniform(1, 2), click_y + random.uniform(1, 2))
                time.sleep(0.02)
                break

    if time.time() - last_check_time > 8 and input_button.lower() == 'y':
        last_check_time = time.time()
        click(win_rect[0] + random.randint(348, 352), win_rect[1] + random.randint(608, 612))
        time.sleep(0.1)


input("Press Enter to Exit...")

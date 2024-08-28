from pynput.mouse import Button, Controller
from ctypes import windll
from loguru import logger
from sys import stderr
import pyautogui
import pygetwindow as gw
import keyboard
import random
import time
import os

mouse_controller = Controller()

def pixel_condition(r, g, b):
    return ((r in range(95, 210) and g in range(205, 255) and b in range(0, 120)) or
            (r in range(70, 130) and g in range(150, 220) and b in range(200, 235))) # color for freezing


windll.kernel32.SetConsoleTitleW('Auto clicker bot for Blum | by https://t.me/dmtrcrypto')

logger.remove()
logger.add(stderr, format='<cyan>{time:HH:mm:ss}</cyan> | <level>{level:<8}</level> | <cyan><bold>{line}</bold></cyan> | <magenta>Message:</magenta> <level><underline>{message}</underline></level>')

print("\n\nTG Channel Creator - https://t.me/dmtrcrypto")

def click(x, y):
    mouse_controller.position = (x, y)
    mouse_controller.press(Button.left)
    mouse_controller.release(Button.left)

input_window_name = input('\nEnter the name of the window with Blum game enabled (Y\y - TelegramDesktop): ')
print("\n")
input_button = input("Do you want the bot to play continuously without your participation until you run out of tickets (Y/n): ")
print("\n")

if input_window_name.lower() == 'y':
    window_name = "TelegramDesktop"
else:
    window_name = input_window_name


check_window = gw.getWindowsWithTitle(window_name)
if not check_window:
    logger.warning(f'The window "{window_name}" was not found')
else:
    telegram_window = check_window[0]
    logger.success(f'The window "{window_name}" was found successfully')
    print("\n")
    logger.info("Use the 'q' button to pause")

paused = True
logger.info('Mode - Stop')

last_check_time = time.time()
image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Button_play.png")
image_start_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Button_play_start.png")

while True:
    if keyboard.is_pressed('q'):
        paused = not paused
        if paused:
            logger.info('Mode - Stop')
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

    screenshot = pyautogui.screenshot(region=win_rect)
    width, height = screenshot.size

    for x in range(0, width, 25): # parameters for slowing down the bot
        for y in range(0, height, 25): # parameters for slowing down the bot
            r, g, b = screenshot.getpixel((x, y))
            if pixel_condition(r, g, b):
                click_x = win_rect[0] + x
                click_y = win_rect[1] + y
                click(click_x + random.uniform(1, 2), click_y + random.uniform(1, 2))
                time.sleep(0.01) # parameters for slowing down the bot
                break

    if time.time() - last_check_time > 5 and input_button.lower() == 'y':
        last_check_time = time.time()
        try:
            location = pyautogui.locateOnScreen(image_path, region=win_rect, confidence=0.9)
            if location:
                click_x, click_y = pyautogui.center(location)
                click(click_x, click_y)
                logger.success("Play button clicked")
                time.sleep(0.2)

            second_location = pyautogui.locateOnScreen(image_start_path, region=win_rect, confidence=0.9)
            if second_location:
                click_x, click_y = pyautogui.center(second_location)
                click(click_x, click_y)
                logger.success("Play-start button clicked")
                time.sleep(0.2)
                
        except pyautogui.ImageNotFoundException:
            continue

input("Press Enter to Exit...")
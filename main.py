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

def pixel_condition(r, g, b):
    return ((r in range(50, 130) and g in range(90, 125) and b in range(80, 120)) or 
            (r in range(240, 255) and g in range(1, 60) and b in range(165, 220)))


windll.kernel32.SetConsoleTitleW('Auto clicker bot for Blum | by https://t.me/dmtrcrypto')

logger.remove()
logger.add(stderr, format='<cyan>{time:HH:mm:ss}</cyan> | <level>{level:<8}</level> | <cyan><bold>{line}</bold></cyan> | <magenta>Message:</magenta> <level><underline>{message}</underline></level>')

print("\n\n\033[94mTG Channel Creator - https://t.me/dmtrcrypto\033[0m\n")

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

    screenshot = pag.screenshot(region=win_rect)
    width, height = screenshot.size

    pixel_detected = False
    button_detected = False
    last_check_time = time.time()

    if pixel_detected:
        break    

    for x in range(0, width, 20):
        for y in range(200, height, 20):
            r, g, b = screenshot.getpixel((x, y))
            current_time = time.time()
            
            if (y >= 750 and 225 <= x <= 275) and (r, g, b) == (255, 255, 255) and input_button.lower() == 'y' and current_time - last_check_time >= 5:
                logger.info("Play button click.")
                time.sleep(2)
                click_x = win_rect[0] + x
                click_y = win_rect[1] + y
                click(click_x, click_y)
                time.sleep(0.2)
                button_detected = True
                last_check_time = current_time
                break
            
            if pixel_condition(r, g, b):
                click_x = win_rect[0] + x
                click_y = win_rect[1] + y
                click(click_x + random.uniform(1, 2), click_y + random.uniform(1, 2))
                time.sleep(0.001)
                pixel_detected = True
                break
            
        if button_detected:
            break

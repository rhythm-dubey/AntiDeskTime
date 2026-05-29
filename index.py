import time
import random
import argparse
import logging
import threading
from datetime import datetime

import pyautogui
from pyautogui import FailSafeException
from pynput import mouse, keyboard

# ---------------- CONFIG DEFAULTS ---------------- #

DEFAULT_CHECK_INTERVAL = 5
DEFAULT_INACTIVITY_THRESHOLD = 60
DEFAULT_MOVE_DURATION = 0.8
DEFAULT_WORK_START = 9
DEFAULT_WORK_END = 19

pyautogui.FAILSAFE = True

# ---------------- GLOBAL STATE ---------------- #

last_activity_time = time.monotonic()
paused = False
lock = threading.Lock()

# ---------------- LOGGING ---------------- #

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)

logger = logging.getLogger("AntiDeskTime")

# ---------------- ACTIVITY LISTENERS ---------------- #

def update_activity():
    global last_activity_time
    with lock:
        last_activity_time = time.monotonic()

def on_mouse_move(x, y):
    update_activity()

def on_key_press(key):
    update_activity()

def start_activity_listeners():
    mouse.Listener(on_move=on_mouse_move).start()
    keyboard.Listener(on_press=on_key_press).start()

# ---------------- UTILS ---------------- #

def is_within_work_hours(start, end):
    now = datetime.now().hour
    return start <= now < end

def is_inactive(threshold):
    with lock:
        return (time.monotonic() - last_activity_time) >= threshold

def is_safe_position(x, y, width, height, margin=50):
    if x < 0 or y < 0 or x >= width or y >= height:
        return False

    corners = [
        (0, 0),
        (width - 1, 0),
        (0, height - 1),
        (width - 1, height - 1)
    ]

    for corner_x, corner_y in corners:
        dx = x - corner_x
        dy = y - corner_y
        if (dx * dx + dy * dy) <= (margin * margin):
            return False

    return True

def human_like_mouse_move(duration):
    current_x, current_y = pyautogui.position()
    screen_width, screen_height = pyautogui.size()

    for attempt in range(3):
        offset_x = random.randint(-30, 30)
        offset_y = random.randint(-30, 30)
        new_x = current_x + offset_x
        new_y = current_y + offset_y

        if is_safe_position(new_x, new_y, screen_width, screen_height):
            break

        logger.debug("Position too close to corner, regenerating offset")
    else:
        logger.warning("Unable to find safe offset, skipping movement")
        return

    try:
        pyautogui.moveRel(offset_x, offset_y, duration=duration)
    except FailSafeException:
        logger.critical("Failsafe triggered — mouse movement cancelled")
        return

# ---------------- HOTKEY ---------------- #

def toggle_pause():
    global paused
    paused = not paused
    state = "PAUSED" if paused else "RESUMED"
    logger.warning(f"Script {state}")

def start_hotkey_listener():
    keyboard.GlobalHotKeys({
        "<ctrl>+<shift>+p": toggle_pause
    }).start()

# ---------------- MAIN LOOP ---------------- #

def run(args):
    logger.info("Anti Desk Time started")
    logger.info("Press CTRL + SHIFT + P to pause/resume")
    logger.info("Failsafe enabled — move mouse to top-left corner to safely stop")

    start_activity_listeners()
    start_hotkey_listener()

    while True:
        try:
            time.sleep(args.check_interval)

            if paused:
                continue

            if not is_within_work_hours(args.work_start, args.work_end):
                continue

            if is_inactive(args.inactivity_threshold):
                logger.info("Inactivity detected → simulating movement")
                human_like_mouse_move(args.move_duration)
                update_activity()
        except FailSafeException:
            logger.critical("Failsafe triggered — script paused for safety")
            paused = True

# ---------------- ARGUMENTS ---------------- #

def parse_args():
    parser = argparse.ArgumentParser(description="Anti Desk Time Utility")

    parser.add_argument(
        "--check-interval",
        type=int,
        default=DEFAULT_CHECK_INTERVAL,
        help="Seconds between inactivity checks"
    )

    parser.add_argument(
        "--inactivity-threshold",
        type=int,
        default=DEFAULT_INACTIVITY_THRESHOLD,
        help="Seconds of inactivity before action"
    )

    parser.add_argument(
        "--move-duration",
        type=float,
        default=DEFAULT_MOVE_DURATION,
        help="Mouse movement duration in seconds"
    )

    parser.add_argument(
        "--work-start",
        type=int,
        default=DEFAULT_WORK_START,
        help="Work day start hour (24h format)"
    )

    parser.add_argument(
        "--work-end",
        type=int,
        default=DEFAULT_WORK_END,
        help="Work day end hour (24h format)"
    )

    return parser.parse_args()

# ---------------- ENTRY ---------------- #

if __name__ == "__main__":
    try:
        run(parse_args())
    except KeyboardInterrupt:
        logger.info("Anti Desk Time stopped safely")

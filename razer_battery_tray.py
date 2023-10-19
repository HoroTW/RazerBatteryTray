#!/usr/bin/env python3

import os
import sys
from time import sleep
import pystray
from pystray import Icon, Menu, MenuItem
import openrazer.client
import PIL.Image
from functools import lru_cache
import logging

RESIZE_TO_PIXELS = 32
SCALE = (RESIZE_TO_PIXELS, RESIZE_TO_PIXELS)
UPDATE_INTERVAL_IN_SECS = 1 / 5
LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()

logfmt = '%(asctime)s %(levelname)s %(message)s';
datefmt = '%Y-%m-%d %H:%M:%S';

logging.getLogger('PIL').setLevel(logging.WARNING) # Silence PIL logging
logging.basicConfig(level=LOGLEVEL, format=logfmt, datefmt=datefmt)

logging.debug(f"Loglevel: {LOGLEVEL}")
logging.debug("Starting Razer Battery Tray")

real_path = os.path.realpath(__file__) # Finding target of Symlink
script_path = os.path.dirname(real_path)
icons_path = os.path.join(script_path, "icons")

if hasattr(PIL.Image, "Resampling"):  # Pillow >= 9.1.0
    DOWNSCALE_METHOD = PIL.Image.Resampling.LANCZOS
else:  # Pillow < 9.1.0
    DOWNSCALE_METHOD = PIL.Image.LANCZOS

try:
    logging.debug(f"Pillow version: {PIL.__version__}")
    logging.debug(f"Openrazer version: {openrazer.client.__version__}")
    logging.debug(f"Python version: {sys.version}")
    logging.debug(f"Path of the icons: {icons_path}")
    
    try:
        if sys.version_info < (3, 8):
            raise Exception("Python 3.8 or higher is required")
        from importlib.metadata import version
        logging.debug(f"Pystray version: {version('pystray')}")
    except:
        logging.warning("Cannot get pystray version (Python 3.8+ is required for that..)")
except:
    logging.error("Failed to get all version infos, please check your installation")


mgr = openrazer.client.DeviceManager()
if len(sys.argv) < 2:
    print("\n!! OOPS: Missing device name as argument !!\n")
    print("Usage: razer_bat_tray.py <part_of_the_device_name>")
    print("Example 1: razer_bat_tray.py 'Razer Viper Ultimate'")
    print("Example 2: razer_bat_tray.py 'DeathAdder'\n")

    print("Listing Available Devices:")
    for dev in mgr.devices:  # print all bat devices
        print(dev.name, "\n    Has Battery:", dev.has("battery"))
    sys.exit(1)

device_name_param = sys.argv[1].lower()
device = None

for dev in mgr.devices:  # find the device we want to monitor
    if device_name_param in dev.name.lower():
        device = dev
        print("Found device:", dev.name)
        break

if device is None:
    logging.error("Device not found, check the name and try again.")
    sys.exit(1)


@lru_cache(maxsize=256)
def get_icon(bat_level, charging=False):
    """
    Get the icon for the given battery level
    """
    name = f"bat_{bat_level}.png" if not charging else f"bat_{bat_level}_c.png"
    icon_path = os.path.join(icons_path, name)
    icon = PIL.Image.open(icon_path).resize(SCALE, DOWNSCALE_METHOD)
    return icon


def setup_icon(icon):
    icon.visible = True
    sleep(1)  # wait for the icon to be visible
    bat_level = device.battery_level
    is_charging = device.is_charging

    logging.debug("Animating icon to current battery level")
    for i in range(100, 0, -4):
        icon.icon = get_icon(i)
        sleep(1 / 30)
    for i in range(0, bat_level + 1, 2):
        icon.icon = get_icon(i)
        sleep(1 / 30)
    logging.debug(f"Icon set to {bat_level}% {'(charging)' if is_charging else ''}")

    # start the update loop
    while True:
        bat_level = device.battery_level
        is_charging = device.is_charging
        cur_icon = get_icon(bat_level, is_charging)
        if cur_icon != icon.icon:
            icon.icon = cur_icon
            logging.debug(f"Icon set to {bat_level}% {'(charging)' if is_charging else ''}")
        sleep(UPDATE_INTERVAL_IN_SECS)


tray_icon = Icon(
    "BatteryIcon",
    get_icon(100),
    menu=Menu(MenuItem(f'Exit Battery Viewer of "{device.name}"', lambda: os._exit(0))),
)

tray_icon.run(setup=setup_icon)

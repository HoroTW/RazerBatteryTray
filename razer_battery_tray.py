#!/usr/bin/env python3

import os
import sys
from time import sleep
import pystray
from pystray import Icon, Menu, MenuItem
import openrazer
import openrazer.client
import PIL.Image

RESIZE_TO_PIXELS = 32
UPDATE_INTERVAL_IN_SECS = 2

print("Starting Razer Battery Tray")

script_path = os.path.dirname(__file__)
icons_path = os.path.join(script_path, "icons")

try:
    print("Pillow version: ", PIL.__version__)
    print("Pystary version: ", pystray.__version__)
    print("Openrazer version: ", openrazer.__version__)
    print("Python version: ", sys.version)
    print("Path of the icons:", icons_path)
except:
    print("Failed to get version info, please check your installation")


a = openrazer.client.DeviceManager()
if len(sys.argv) < 2:
    print("Missing device name as argument")
    print("Usage: razer_bat_tray.py <part_of_the_device_name>")
    print("Example: razer_bat_tray.py 'Razer Viper Ultimate'\n")

    print("Listing Available Devices:")
    for dev in a.devices:  # print all bat devices
        print(dev.name, "\n    Has Battery:", dev.has("battery"))
    sys.exit(1)

device_name_param = sys.argv[1].lower()
device = None

for dev in a.devices:  # find the device we want to monitor
    if device_name_param in dev.name.lower():
        device = dev
        print("Found device:", dev.name)
        break

if device is None:
    print("Device not found, check the name and try again, maybe use less of the name?")
    sys.exit(1)


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

    # animate the icon to current battery level
    for i in range(100, 0, -3):
        icon.icon = get_icon(i)
        sleep(0.02)
    for i in range(0, device.battery_level + 1, 2):
        icon.icon = get_icon(i)
        sleep(0.03)

    # start the update loop
    while True:
        bat_level = device.battery_level
        icon.icon = get_icon(bat_level, device.is_charging)
        print(f"Icon set to {bat_level} %")
        sleep(UPDATE_INTERVAL_IN_SECS)


tray_icon = Icon(
    "BatteryIcon",
    get_icon(100),
    menu=Menu(MenuItem(f'Exit Battery Viewer of "{device.name}"', lambda: os._exit(0))),
)

tray_icon.run(setup=setup_icon)

import sys
import os
from time import sleep

from dbus import DBusException
from logger import logger
from functools import lru_cache
import openrazer.client
import pystray
from pystray import Icon, Menu, MenuItem
import PIL.Image


class RazerBatteryTrayManager:
    def __init__(self, icon_path, update_interval_in_secs, scale):
        logger.debug("Creating RazerBatteryTrayManager")
        try:
            logger.debug(f"Python version: {sys.version}")
            logger.debug(f"Openrazer version: {openrazer.client.__version__}")
            logger.debug(f"Pillow version: {PIL.__version__}")
            try:
                if sys.version_info < (3, 8):
                    raise Exception("Python 3.8 or higher is required")
                from importlib.metadata import version

                logger.debug(f"Pystray version: {version('pystray')}")
            except:
                logger.warning(
                    "Cannot get pystray version (Python 3.8+ is required for that..)"
                )
        except:
            logger.warning(
                "Failed to get all version infos, please check your installation"
            )
            sys.exit(1)

        if hasattr(PIL.Image, "Resampling"):  # Pillow >= 9.1.0
            self.downscale_method = PIL.Image.Resampling.LANCZOS
        else:  # Pillow < 9.1.0
            self.downscale_method = PIL.Image.LANCZOS

        self.mgr = openrazer.client.DeviceManager()
        self.device = None
        logger.debug(f"Path of the icons: {icon_path}")
        self.iconpath = icon_path
        self.update_interval_in_secs = update_interval_in_secs
        self.scale = scale

    def activate(self):
        logger.debug("Activating tray icon")
        if self.device is None:
            raise Exception("Device not found, check the name and try again.")

        tray_icon = Icon(
            "BatteryIcon",
            self.get_icon(100),
            title=f"{self.device.name}",
            menu=Menu(
                MenuItem(
                    f'Exit Battery Viewer of "{self.device.name}"', lambda: os._exit(0)
                )
            ),
        )
        tray_icon.run(setup=self.setup_icon)

    def list_devices(self, list_all=False, verbose=True):
        print("Listing Available Devices:") if verbose else None

        for dev in self.mgr.devices:  # print all bat devices
            if dev.has("battery") or list_all:
                print(dev.name)
                print("    Has Battery:", dev.has("battery")) if verbose else None

    def set_device_from_name(self, part_of_device_name: str):
        logger.debug(f"Setting device from name {part_of_device_name}")
        for dev in self.mgr.devices:  # find the device we want to monitor
            if part_of_device_name in dev.name.lower():
                logger.info(f"Found device: '{dev.name}'")
                self.device = dev

    @lru_cache(maxsize=256)
    def get_icon(self, bat_level, charging=False):
        """
        Get the icon for the given battery level
        """
        name = f"bat_{bat_level}.png" if not charging else f"bat_{bat_level}_c.png"
        icon_path = os.path.join(self.iconpath, name)
        icon = PIL.Image.open(icon_path).resize(self.scale, self.downscale_method)
        return icon

    def setup_icon(self, icon):
        icon.visible = True
        sleep(1)  # wait for the icon to be visible
        bat_level = self.device.battery_level
        is_charging = self.device.is_charging

        logger.debug("Animating icon to current battery level")
        for i in range(100, 0, -4):
            icon.icon = self.get_icon(i)
            sleep(1 / 30)
        for i in range(0, bat_level + 1, 2):
            icon.icon = self.get_icon(i)
            sleep(1 / 30)
        logger.debug(f"Icon set to {bat_level}% {'(charging)' if is_charging else ''}")

        # start the update loop
        while True:
            try:
                bat_level = self.device.battery_level
                is_charging = self.device.is_charging
            except:
                logger.debug("Device currently not connected --> hiding icon")
                icon.icon = self.get_icon(0)  # (0% is better than the last icon)
                sleep(1)  # some desktops need a little time to hide the icon
                icon.visible = False # this hides the icon into the overflow of the tray
                sleep(2)  # additional 5s sleep to not recheck too often
                continue

            if icon.visible == False:
                logger.debug("Device (re)connected --> showing icon")
                icon.visible = True
                sleep(1) # some desktops need a little time to show the icon again
                icon.icon = self.get_icon(
                    bat_level, is_charging
                )  # needed to update the icon

            cur_icon = self.get_icon(bat_level, is_charging)
            if cur_icon != icon.icon:
                icon.icon = cur_icon
                logger.debug(
                    f"Icon set to {bat_level}% {'(charging)' if is_charging else ''}"
                )
            sleep(self.update_interval_in_secs)

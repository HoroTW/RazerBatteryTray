#!/usr/bin/env python3

import os
import sys
from logger import logger
from pathlib import Path
from argument_parser import ArgumentParser
from rbt_manager import RazerBatteryTrayManager

RESIZE_TO_PIXELS = 32
UPDATE_INTERVAL_IN_SECS = 1 / 5

executable_name = os.path.basename(__file__)  # Name of the executable or SymLink used
real_path = os.path.realpath(__file__)  # Finding target of Symlink
script_path = Path(os.path.dirname(real_path))
icon_path = os.path.join(script_path.parent, "icons")

if __name__ == "__main__":
    action, options, part_of_device_name = ArgumentParser(executable_name).parse_args()
    logger.debug(f"Parsed arguments: {action}, {options}, {part_of_device_name}")

    rbtm = RazerBatteryTrayManager(
        icon_path=icon_path,
        update_interval_in_secs=UPDATE_INTERVAL_IN_SECS,
        scale=(RESIZE_TO_PIXELS, RESIZE_TO_PIXELS),
    )

    if action == "list":
        rbtm.list_devices(list_all=False, verbose=options["verbose"])
    elif action == "list-all":
        rbtm.list_devices(list_all=True, verbose=options["verbose"])
    else:
        rbtm.set_device_from_name(part_of_device_name)
        rbtm.activate()  # start the tray icon loop

    sys.exit(0)

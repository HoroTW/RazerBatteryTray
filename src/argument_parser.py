import sys
import os
from logger import logger

class ArgumentParser:
    """
    A simple argument parser for the vanish script.
    executable_name: The name of the executable, used for the help message.
    """

    def __init__(self, executable_name: str):
        self.executable_name = executable_name

    def print_usage_and_exit(self, exit_code: int):
        """Prints the usage and exits with the given exit code."""
        self.print_usage()
        sys.exit(exit_code)

    def print_usage(self):
        """Prints the usage"""
        print(
            f"""
Usage: {self.executable_name} [OPTIONS] <part_of_the_device_name>

OPTIONS:
  --help, -h                Print this help message
  --list, -l                List all available devices
  --list-all, -a            Lists all devices even if they don't have a battery
  --parsable, -p            Be less verbose so that the output is easier to parse
  --quit-on-disconnect, -q  Quit when the device is disconnected (instead of waiting for a reconnect)

  <part_of_the_device_name>: The name of the device to use. Can be a substring of
                             the full device name.
EXAMPLES:
  Example 1: {self.executable_name} 'Razer Viper Ultimate'
  Example 2: {self.executable_name} 'DeathAdder'

DESCRIPTION:
  Razer Battery Tray
  ------------------
  A tray icon for the battery level of Razer mice and keyboards which are
  supported by OpenRazer.
"""
        )

    def parse_args(self):
        action = None # the action to perform
        part_of_the_device_name = None
        options = {"verbose": True, "quit_on_disconnect": False}

        # check if an arg is --help
        if any( (arg == "--help" or arg == "-h") for arg in sys.argv):
            self.print_usage_and_exit(0)

        # start normal argument parsing
        i = 0
        while i < len(sys.argv):
            arg = sys.argv[i] # the current argument

            if arg == "--list" or arg == "-l":
                sys.argv.pop(i)
                action = "list"
            elif arg == "--list-all" or arg == "-a":
                sys.argv.pop(i)
                action = "list-all"
            elif arg == "--parsable" or arg == "-p":
                sys.argv.pop(i)
                options["verbose"] = False # it is better parsable if it is less verbose
            elif arg == "--quit-on-disconnect" or arg == "-q":
                sys.argv.pop(i)
                options["quit_on_disconnect"] = True
            else:
                i += 1

        if action is not None:
            return action, options, part_of_the_device_name        
            
        # check if part_of_the_device_name is given
        if len(sys.argv) < 2:
            logger.error("Missing part of the device name as argument.")
            self.print_usage_and_exit(1)
        elif len(sys.argv) > 2:
            logger.error("Too many arguments given.")
            logger.debug(f"Arguments: {sys.argv}")
            self.print_usage_and_exit(1)

        part_of_the_device_name = sys.argv[1].lower()
        return action, options, part_of_the_device_name

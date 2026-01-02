# RazerBatteryTray
A few scripts to show the battery state of a Razer device in the tray (Percent / Loading). 
Leverages 
- Openrazer
- Pillow
- pystray

![Screenshot](screenshots/Screenshot_01.png)

![gif](screenshots/gif_razer_battery_tray.gif)

## Latest update
### Added
- `--list`, `--list-all` (all devices including those without battery) and `--parsable` (be less verbose) options.
- `razer-battery-icon --list --parsable` gives now:
   Razer Naga Pro (Wired/Wireless)

### Fixes
- Fixed crash on device disconnect.
  Added a `--quit-on-disconnect` for people who prefer the old way (e.g. you could restart the script on device connect using udev rules)
  The default is that the script hides the icon into the overflow and sets the battery percentage to 0% and waits for the device to come back ^^

### Improvements:
- Logging support:
  Loglevel can be controlled using an env var like that `LOG_LEVEL=DEBUG` Possible is ERROR, WARNING (default), INFO, DEBUG
-  Tray Icon hover over shows now the device name
-  Added a cache and a sleep detection for devices so the battery does not show 0 when device goes to sleep.


| Discharging Icon | Discharging Icon | Discharging Icon | Charging Icon |
| --- | --- | --- | --- |
![Example Battery Icon](icons/bat_12.png) | ![Example Battery Icon](icons/bat_34.png) | ![Example Battery Icon](icons/bat_84.png) | ![Example Battery Icon while Charging](icons/bat_43_c.png)


**If you like these small script a ⭐ star would be really nice 😉**

## Pre-requisites
So you need to install Openrazer in your system.
Additionally you need Pillow and pystray. 

You can install them with pip:

```
python -m pip install pillow pystray
```

Note:
For some wayland desktops you might need to install appindicator to get the tray icon: [Link to the pystray documentation](https://pystray.readthedocs.io/en/latest/usage.html#supported-backends)

If you have issues with displaying the tray icon search for your desktop environment and appindicator to find out which one you might need.

## Installation
Just copy the scripts to your system and make them executable.

### Manual installation for most linux systems:

```bash
git clone https://github.com/HoroTW/RazerBatteryTray.git
cd RazerBatteryTray
chmod +x razer_battery_tray.py
```
### NixOS installation
Beside the same setup as above you have to install `openrazer daemon` following
the [official guide](https://openrazer.github.io/#nixos).

If you use `GNOME` with `WAYLAND` you have to also add and **MANUALLY!!** turn on the extension.
```nix
  environment.systemPackages = [
    pkgs.gnomeExtensions.appindicator
  ];
```
In the `Extensions` app the extension is called `AppIndicator and KStatusNotifierItem Support`.

To get the client working, you need some more packages.
For use with a `nix-shell` here is a example `shell.nix`:
```nix
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3Packages.openrazer
    pkgs.python3Packages.pystray
    pkgs.python3Packages.pillow
    pkgs.libappindicator
  ];
}
```

## Usage
Just run the script and it will tell you about devices that you can use.

Then run it with a part of the device name as argument.

```bash
./razer_battery_tray.py

Missing device name as argument
Usage: razer_battery_tray.py <part_of_the_device_name>
Example: razer_battery_tray.py 'Razer Viper Ultimate'

Listing Available Devices:
Razer Viper Ultimate (Wireless) 
    Has Battery: True
Razer Mouse Dock 
    Has Battery: False


./razer_battery_tray.py 'Razer Viper Ultimate'
Found device: Razer Viper Ultimate (Wireless)
Icon set to 85 %
```

Then you just need to autostart it on login with your DE or similar.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Hope you like it :)

~HoroTW

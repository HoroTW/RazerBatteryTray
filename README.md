# RazerBatteryTray
A few scripts to show the battery state of a Razer device in the tray (Percent / Loading). 
Leverages 
- Openrazer
- Pillow
- pystray

![Screenshot](screenshots/Screenshot_01.png)

![gif](screenshots/gif_razer_battery_tray.gif)


| Discharging Icon | Discharging Icon | Discharging Icon | Charging Icon |
| --- | --- | --- | --- |
![Example Battery Icon](icons/bat_12.png) | ![Example Battery Icon](icons/bat_34.png) | ![Example Battery Icon](icons/bat_84.png) | ![Example Battery Icon while Charging](icons/bat_43_c.png)


## Pre-requisites
So you need to install Openrazer in your system.
Additionally you need Pillow and pystray. 

You can install them with pip:

```
python -m pip install pillow pystray
```

## Installation
Just copy the scripts to your system and make them executable.

### Manual installation for most linux systems:

```bash
git clone https://github.com/HoroTW/RazerBatteryTray.git
cd RazerBatteryTray
chmod +x razer_battery_tray.py
```
### NixOS installation::
Beside the same setup as above, you need these lines in your `configuration.nix`:
You have to install `openrazer daemon` following the [official guide](https://openrazer.github.io/#nixos).

To get the client working, you need the following packages. 
 - libappindicator
 - python3Packages.openrazer
 - python3Packages.pystray
 - python3Packages.pillow

For use with a `nix-shell` here is a example `shell.nix`:
```nix
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.openrazer-daemon
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
Usage: razer_bat_tray.py <part_of_the_device_name>
Example: razer_bat_tray.py 'Razer Viper Ultimate'

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

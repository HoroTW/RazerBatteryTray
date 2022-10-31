# RazerBatteryTray
A few scripts to show the battery state of a Razer device in the tray (Percent / Loading). 
Leverages 
- Openrazer
- Pillow
- pystray

![Screenshot](Screenshot_01.png)

![gif](screenshots/gif_razer_battery_tray.gif)

![Example Battery Icon](icons/bat_84.png) ![Example Battery Icon while Charging](icons/bat_84_c.png)


## Pre-requisites
So you need to install Openrazer in your system.
Additionally you need Pillow and pystray. 

You can install them with pip:

```
python -m pip install pillow pystray
```

## Installation
Just copy the scripts to your system and make them executable.

```bash
git clone git@github.com:HoroTW/RazerBatteryTray.git
cd RazerBatteryTray
chmod +x razer_battery_tray.py
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

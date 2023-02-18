# AutomaticDesktopRotation
Make your OS automatically rotate your display when you physically rotate your monitor. Supports multiple monitors with minimal setup and Wallpaper Engine.
## Arduino Setup
Note: The only Arduino I own is the Nano 33 BLE. This should work with other boards as well, but you may need to modify the script to read the data from your accelerometer. 

1. [Install the latest version of the Arduino IDE](https://www.arduino.cc/en/software).
2. Open NanoBLE.ino in the Arduino IDE, then go to Tools > Library Manager, and install 'Arduino_LSM9DS1'.
3. Set `displayID` to the ID of the monitor your Arduino will be connected to. To get this number in Windows, you can open the Settings app, and take the monitor ID shown there. This process is (probably) similar for Linux.
4. Upload the sketch. You can use the serial monitor (Tools > Serial Monitor) to verify that it's working.

## Python Setup
1. Install [Python](https://www.python.org/downloads/) 3.11 or higher.
2. Run `pip install -f requirements.txt` to install the required Python modules.
3. If you want to change where the config file is stored (by default, it's the same folder as AutomaticDesktopRotation.py), set `config_path` to the absolute path of the new location.

### Config 
###### The following instructions are for AutomaticDesktopRotation.toml
1. Set `device_count` to the number of Arduinos you are using.
2. If you use Wallpaper Engine, create a `[monitor.X]` section for each monitor, where X is the monitor ID you used in the Arduino script.
3.  Set `monitor_index` to what Wallpaper Engine thinks the monitor ID is. This should match the ID assigned by the operating system, but if wallpapers are appearing on incorrect monitors, the `monitor_index` probably needs to be changed.
4. `X.path` refers to the absolute path of the wallpaper's project.json file, where X is the angle (0, 90, or 270) that you want the wallpaper to be assigned to. A wallpaper's path can be found by right-clicking it in Wallpaper Engine and selecting "Open in Explorer". 
5. `X.name` should be used to store the name of the wallpaper.

The datatype of a value matters in TOML files. The included config can be used as a reference, but make especially sure to either enclose file paths in single quotes to parse it as a raw string, or escape the backslashes with a second backslash. Failure to do so will result in a parser error and require a script restart.

Here's an example config for monitor 1:
```
[monitor.1]
monitor_index = 1
0.name = 'Goat'
0.path = 'H:\SteamLibrary\steamapps\workshop\content\431960\2376779016\project.json'
90.name = 'Garfield'
90.path = 'H:\SteamLibrary\steamapps\workshop\content\431960\2208437588\project.json'
270.name = 'Life could be dream'
270.path = 'H:\SteamLibrary\steamapps\workshop\content\431960\2512005692\project.json'
```

#### Windows
There are two methods this script can use to rotate your monitor on Windows: The pywin32 Python module (this is used by default) and display64.exe.

While they are functionally the same, I've noticed that while using pywin32, if you rotate your monitor from 90 to 270 degrees without letting Windows
rotate to 0 degrees partway through, the screen wouldn't rotate. Display64.exe does not have this issue.

There may be other scenarios where one is better than the other, so give them both a try.

To use display64.exe instead of pywin32:
1. Download it from [here](http://noeld.com/programs.asp?cat=misc#display). While it is free to download, buy a copy if you can to support the creator. 
2. In the config, set `windows_fallback` to `True` and set `displayexe` to wherever you've extracted display64.exe to.

To make AutomaticDesktopRotation.py start on boot: 
1. Move AutomaticDesktopRotation.py to `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\ ` and AutomaticDesktopRotation.toml to a non-startup folder.
2. In AutomaticDesktopRotation.py, change `config_path` to the absolute path of the config file
3. Change the file extension of AutomaticDesktopRotation.py to `.pyw`. 
4. Make sure Windows is set to open .pyw files by right-clicking AutomaticDesktopRotation.pyw, selecting 'open with', checking 'always use this app to open .pyw files', and selecting pythonw.exe, located in `AppData\Local\Programs\Python\Python311`. 

#### Linux
###### While these instructions are somewhere in the realm of "correct", they have not been tested and may need adjustments to work.
1. Install xrandr using your distro's package manager.<br>
Debian-based: `sudo apt install xrandr`<br>
Arch-based: `sudo pacman xorg-xrandr`<br>
rpm-based: `sudo dnf install xrandr`
2. To make AutomaticDesktopRotation.py start on boot:<br>
    1. Run `sudo nano /etc/systemd/system/AutoScreenRotation.service`
    2. Paste the following text, replacing {python path} and {script path} appropriately.
```
[Unit]
Description="Automatic screen rotation"

[Service]
ExecStart={python path} {script path}/AutomaticDesktopRotation.py

[Install]
WantedBy=multi-user.target
```
3. Reload the daemon.<br>
`sudo systemctl daemon-reload`<br>
4. Enable the service.<br>
`sudo systemctl enable AutoScreenRotation.service`<br>
5. Start the service.<br>
`sudo systemctl start AutoScreenRotation.service`<br>
4. Make sure to modify the xrandr command in AutomaticDesktopRotation.py as needed, as it isn't tested and may need adjustments to work.

## Mounting the Arduino on your monitor

Your Arduino Nano should have its USB port pointing down, and its reset button facing outwards like this:

<img src="https://user-images.githubusercontent.com/33820904/167181039-eb83da52-78ec-4961-87ce-9b6d54d1de27.jpg" width="500">


## Demo

https://user-images.githubusercontent.com/33820904/167163670-3158abf7-d2fd-440a-8990-3475fdbc0dc9.mp4

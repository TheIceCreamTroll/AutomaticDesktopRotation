# AutomaticDesktopRotation
Make your OS automatically rotate your display when you physically rotate your monitor. Supports multiple monitors with minimal setup.
## Arduino Setup
Note: The only Arduino I own is the Nano 33 BLE. This should work with other boards as well, though you may need to modify the script to read the data from your accelerometer. 

1. [Install the latest version of the Arduino IDE](https://www.arduino.cc/en/software).
2. Open NanoBLE.ino in the Arduino IDE, then go to Tools > Library Manager, and install 'Arduino_LSM9DS1'.
3. Set ```displayID``` to the ID of the monitor your Arduino will be connected to. To get this number in Windows, you can open the Settings app, and take the monitor ID shown there. This process is probably similar on Linux.
4. Upload the sketch. You can use the serial monitor (Tools > Serial Monitor) to verify that it's working.

## Python Setup

1. Install your OS's required Python modules with: ```pip install -f requirements.txt```<br>

2. In AutomaticDesktopRotation.py, set ```DeviceCount =``` to the number of Arduinos you are using.
#### Windows
To make AutoScreenRotation.py start on boot: 
1. Move AutoScreenRotation.py to ```%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\```
2. Change the file extension to .pyw. 
3. Make sure Windows is set to open .pyw files by right-clicking AutoScreenRotation.pyw, selecting 'open with', checking 'always use this app to open .pyw files', and selecting pythonw.exe, located in ```AppData\Local\Programs\Python\Python310```. 
    

#### Linux
1. Install xrandr using your distro's package manager.<br>
Debian-based: ```sudo apt install xrandr```<br>
Arch-based: ```sudo pacman xorg-xrandr```<br>
rpm-based: ```sudo dnf install xrandr```
2. To make AutoScreenRotation.py start on boot:<br>
    1. Run ```sudo nano /etc/systemd/system/AutoScreenRotation.service```
    2. Paste the following text, replacing {python path} and {script path} appropriately.
```
[Unit]
Description="Automatic screen rotation"

[Service]
ExecStart={python path} {script path}/AutoScreenRotation.py

[Install]
WantedBy=multi-user.target
```
3. Reload the daemon.<br>
```sudo systemctl daemon-reload```<br>
4. Enable the service.<br>
```sudo systemctl enable AutoScreenRotation.service```<br>
5. Start the service.<br>
```sudo systemctl start AutoScreenRotation.service```<br>
4. Make sure to modify the xrandr command in AutomaticDesktopRotation.py as needed, as I haven't actually tested it yet (not a Linux user), and it's probably borked.

## Mounting the Arduino on your monitor

Your Arduino Nano should have its USB port pointing down, and its reset button facing outwards. Find some way to secure it, and you're done. 

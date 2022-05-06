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

There are two methods this script can use to rotate your monitor on Windows: The pywin32 Python module (this is used by default) and display64.exe.

While they are functionally the same, I've noticed that while using pywin32, if you rotate your monitor from 90 to 270 degrees without letting Windows
rotate to 0 degrees partway through, the screen wouldn't rotate. Display64.exe does not have this issue.

There may be other scenarios where one is better than the other, so give them both a try.

To use display64.exe instead of pywin32:
1. Download it from [here](http://noeld.com/programs.asp?cat=misc#display). While it's free to download, buy a copy if you can to support the creator. 
2. Set ```windowsfallback``` to ```True``` and set ```displayexe =``` to wherever you've extracted display64.exe to.

To make AutomaticDesktopRotation.py start on boot: 
1. Move AutomaticDesktopRotation.py to ```%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\```
2. Change the file extension to .pyw. 
3. Make sure Windows is set to open .pyw files by right-clicking AutomaticDesktopRotation.pyw, selecting 'open with', checking 'always use this app to open .pyw files', and selecting pythonw.exe, located in ```AppData\Local\Programs\Python\Python310```. 
    

#### Linux
1. Install xrandr using your distro's package manager.<br>
Debian-based: ```sudo apt install xrandr```<br>
Arch-based: ```sudo pacman xorg-xrandr```<br>
rpm-based: ```sudo dnf install xrandr```
2. To make AutomaticDesktopRotation.py start on boot:<br>
    1. Run ```sudo nano /etc/systemd/system/AutoScreenRotation.service```
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
```sudo systemctl daemon-reload```<br>
4. Enable the service.<br>
```sudo systemctl enable AutoScreenRotation.service```<br>
5. Start the service.<br>
```sudo systemctl start AutoScreenRotation.service```<br>
4. Make sure to modify the xrandr command in AutomaticDes


ktopRotation.py as needed, as I haven't actually tested it yet (not a Linux user), and it's probably borked.

## Mounting the Arduino on your monitor

Your Arduino Nano should have its USB port pointing down, and its reset button facing outwards. Find some way to secure it, and you're done. 

## Demo




https://user-images.githubusercontent.com/33820904/167067854-a62818c5-4ff4-46eb-9599-8bb2a529af55.mp4



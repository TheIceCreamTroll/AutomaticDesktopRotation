import serial
from time import sleep
from sys import platform
from subprocess import run
from threading import Thread
from traceback import print_exc
import serial.tools.list_ports as listports

######## Edit these values as needed ##############

# Number of Arduinos being used.
DeviceCount = 1

# Enable this to print stuff to console. Wouldn't do anything while running in the background.
quiet = True

# If, for whatever reason, the win32api rotation method doesn't work,
# this is a functionally equivalent fallback. Set displayexe to wherever you've placed display64.exe.
windowsfallback = False
displayexe = ""

###################################################

# The OS determines which method we use to rotate the screen.
if platform.startswith('win32'):
    if not windowsfallback:
        import win32api as win32
        import win32con
    operatingSystem = "windows"
else:
    operatingSystem = "linux"  # OSX can use xrandr via MacPorts. FreeBSD should be able to use it as well.


def log(msg):
    if not quiet:
        print(msg)


def initSerial(dev):
    ser = serial.Serial(dev, 9600, timeout=1, xonxoff=False, rtscts=False, dsrdtr=False)
    ser.flushInput()
    ser.flushOutput()
    return ser


def waitForSerialInit():
    possibleDevices = []

    ports = listports.comports()
    for port, desc, hwid in sorted(ports):
        possibleDevices.append(port)

    while True:
        for dev in possibleDevices:
            try:
                ser = initSerial(dev)
                log("device found on " + dev)
                return ser
            except Exception:
                log("Failed to initialize device on " + dev)
                continue
        sleep(5)


def RotationProcess():
    # Initialize at 0 degrees
    old = "0"
    ser = waitForSerialInit()

    while True:
        try:
            line = ser.readline().decode("utf-8")
        except Exception:
            log("error: ")
            print_exc()
            log("probably not plugged in")
            sleep(5)
            log("trying to init serial again")
            ser = waitForSerialInit()
            continue

        if len(line) != 0:
            try:
                line = line.strip().split()
                log(line)

                displayID = int(line[0]) - 1
                angle = float(line[1])

                if angle <= -40:
                    #log("Pointing left")
                    current = "270"

                if -40 <= angle <= 40:
                    #log("Pointing up")
                    current = "0"

                if 40 <= angle:
                    #log("Pointing right")
                    current = "90"

                if current != old:
                    if operatingSystem == "windows":
                        if windowsfallback:
                            run("'" + displayexe + "' /device " + str(displayID) + " /rotate " + str(current), shell=True)
                        else:
                            device = win32.EnumDisplayDevices(None, displayID)
                            dm = win32.EnumDisplaySettings(device.DeviceName, win32con.ENUM_CURRENT_SETTINGS)

                            if current == "0":
                                log("Rotating to 0 degrees")
                                dm.DisplayOrientation = win32con.DMDO_DEFAULT
                            elif current == "90":
                                log("Rotating to 90 degrees")
                                dm.DisplayOrientation = win32con.DMDO_90
                            elif current == "270":
                                log("Rotating to 270 degrees")
                                dm.DisplayOrientation = win32con.DMDO_270

                            dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth
                            win32.ChangeDisplaySettingsEx(device.DeviceName, dm)

                    else: # I (do not) use Arch btw, so this may not be the most optimal solution, or even work.
                        run("xrandr --output HDMI1 --rotate " + current + " &", shell=True)  # --screen [deviceID] ?

                    old = current
            
            # Turning a monitor off will cause an exception to be thrown.
            except Exception as e:
                log(e)
                continue

# Start a thread for each device.
threads = []
for monitor in range(DeviceCount):
    t = Thread(target=RotationProcess).start()
    threads.append(t)

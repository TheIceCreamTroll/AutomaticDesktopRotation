import serial
from time import sleep
from sys import platform
from subprocess import run
from threading import Thread
from traceback import print_exc
import serial.tools.list_ports as listports

######## Edit these values as needed ##############

# Only disable this for debugging.
quiet = True

# Number of Arduinos being used.
DeviceCount = 2

# Alternative rotation method.
windowsfallback = False
displayexe = "display64.exe" # Path to display64.exe

###################################################

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
    while True:
        possibleDevices = []
        ports = listports.comports()
        for port, desc, hwid in sorted(ports):
            possibleDevices.append(port)

        for dev in possibleDevices:
            log(f"Dev: {dev}")
            try:
                log(possibleDevices)
                ser = initSerial(dev)
                log(f"device found on {dev}")
                return ser
            except Exception:
                log(f"Failed to initialize device on {dev}")
                continue
        log("Sleeping for 5 secomds")
        sleep(5)


def RotationProcess():

    ser = waitForSerialInit()
    old_angle = 0

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

                displayID = int(line[0])
                angle = float(line[1])

                if angle <= -40:
                    log("Pointing left")
                    current = "270"

                if -40 <= angle <= 40:
                    log("Pointing up")
                    current = "0"

                if 40 <= angle:
                    log("Pointing right")
                    current = "90"

                if current != old_angle:
                    if operatingSystem == "windows":
                        if windowsfallback:
                            run(f"{displayexe} /device {displayID} /rotate {current} /display none", shell=True)
                        else:
                            device = win32.EnumDisplayDevices(None, displayID - 1)
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
                        run(f"xrandr --output HDMI1 --rotate {current} &", shell=True)  # --screen [deviceID] ?

                    old_angle = current

            # Turning a monitor off will cause an exception to be thrown.
            except Exception as e:
                log(e)
                continue

# Start a thread for each device.
threads = []
for monitor in range(DeviceCount):
    t = Thread(target=RotationProcess).start()
    threads.append(t)

import re
import time
import serial
import tomllib
from time import sleep
from sys import platform
from pathlib import Path
from subprocess import run
from threading import Thread
from traceback import print_exc
import serial.tools.list_ports as listports


# Absolute path to the config file
config_path = __file__

config_name = "AutomaticDesktopRotation.toml"

############################################ No Settings Beyond This Point ############################################


class Config:
    def __init__(self):
        self.config_path = Path(config_path).parent / config_name
        self.config_mtime = 0
        self.config = None
        self.refresh_needed = True  # Do a refresh on startup to make sure any changes to the wallpapers get reflected
        self.load_config()

    def load_config(self):
        with open(self.config_path, "rb") as f:
            config = tomllib.load(f)

            if not self.config:
                self.config = config

            if self.config != config and config is not None:
                self.refresh_needed = True

            self.config = config

        self.quiet = config['quiet']
        self.displayexe = config['displayexe']
        self.device_count = config['device_count']
        self.windows_fallback = config['windows_fallback']
        self.enable_wallpaper_engine = config['enable_wallpaper_engine']

        self.config_mtime = Path(self.config_path).stat().st_mtime

    def reload_config(self):
        if self.config_path.stat().st_mtime > self.config_mtime:
            self.load_config()


def log(msg):
    if not global_config.quiet:
        print(msg)


def initSerial(dev):
    ser = serial.Serial(dev, 9600, timeout=1, xonxoff=False, rtscts=False, dsrdtr=False)
    ser.flushInput()
    ser.flushOutput()
    return ser


def waitForSerialInit():
    while True:
        possible_devices = []
        ports = listports.comports()
        for port, desc, hwid in sorted(ports):
            possible_devices.append(port)

        for dev in possible_devices:
            log(f"Dev: {dev}")
            try:
                log(possible_devices)
                ser = initSerial(dev)
                log(f"device found on {dev}")
                return ser
            except Exception:
                log(f"Failed to initialize device on {dev}")
                continue
        log("Sleeping for 5 seconds")
        sleep(5)


def get_wp_path():
    retries = 0
    wp_path = None

    if operating_system == 'windows':
        while not wp_path or retries < 6:
            processes = run(['wmic', 'process', 'get', 'executablepath'], capture_output=True)
            proc_list = processes.stdout.decode().split('\r\r\n')
            wp_path = [i.strip() for i in proc_list if len(i.strip()) and re.search(r'\\wallpaper[0-9][0-9].exe$', i.strip())]

            if wp_path:
                break

            time.sleep(0.5)  # Just in case Wallpaper Engine takes a few seconds to start
            retries += 1
        else:
            raise Exception('Unable to find Wallpaper Engine Process')

        return wp_path[0]
    else:
        # TODO - KDE has a Wallpaper Engine plugin. See if it works with this
        log('Tried to use Wallpaper Engine on a system that does not support it. Doing nothing...')


def wp_rotate(monitor_id, rotation, config):
    if wp_exe:
        wp_name = config.config['monitor'][str(monitor_id)][rotation]['name']
        wp_path = config.config['monitor'][str(monitor_id)][rotation]['path']
        wp_monitor = config.config['monitor'][str(monitor_id)]['monitor_index']

        log(f"Applying wallpaper {wp_name} for monitor {monitor_id}. Path: {wp_path}")
        run([wp_exe, '-control', 'openWallpaper', '-file', wp_path, '-monitor', str(wp_monitor)])
    else:
        log('Could not locate the Wallpaper Engine executable')


def RotationProcess():
    # We need to give each process its own config object or else config refreshes will only occur on one of them
    config = Config()

    ser = waitForSerialInit()
    old_angle = 0

    while True:
        config.reload_config()
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

                display_id = int(line[0])
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

                if current != old_angle or config.refresh_needed:
                    if config.refresh_needed:
                        config.refresh_needed = False

                    if operating_system == "windows":
                        if config.windows_fallback:
                            run(f"{config.displayexe} /device {display_id} /rotate {current} /display none")

                        else:
                            device = win32.EnumDisplayDevices(None, display_id - 1)
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

                    else:  # TODO - eventually test this
                        run(['xrandr', '--output', 'HDMI1', '--rotate', current, '&'])  # --screen [deviceID] ?

                    if config.enable_wallpaper_engine:
                        wp_rotate(display_id, current, config)

                    old_angle = current

            # Turning a monitor off will cause an exception to be thrown.
            except Exception as e:
                log(e)


global_config = Config()

if platform.startswith('win32'):
    if not global_config.windows_fallback:
        import win32api as win32
        import win32con
    operating_system = "windows"
else:
    operating_system = "linux"  # OSX can use xrandr via MacPorts. FreeBSD should be able to use it as well.

if global_config.enable_wallpaper_engine:
    wp_exe = get_wp_path()

log("Starting")
# Start a thread for each device.
threads = []
for monitor in range(global_config.device_count):
    t = Thread(target=RotationProcess).start()
    threads.append(t)

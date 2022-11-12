# -------------------------------
# Author: Yatish Dubasi
# Author: Tyler Spreen
# -------------------------------
import serial
import time
from pynput.keyboard import Listener, Key
import os
import sys
import shutil
import platform
import webbrowser


# -------------------------------
# ----------- Classes -----------
# -------------------------------


# -------------------------------
# ---------- FUNCTIONS ----------
# -------------------------------


# -------------------------------
# ------------ Start ------------
# -------------------------------
# Target URL when door is opened
# https://updatefaker.com/windows11/index.html

temp_directory = "C:/Users/dubas/Desktop/door_update/temp_data"
# Delete temp directory path, then recreate it
shutil.rmtree(temp_directory)
os.mkdir(temp_directory)

# Detect OS system
os_type = platform.system()  # Results can be Linux, Darwin (for mac), Windows
os_release = platform.release()  # Only useful to distinguish between Windows versions, no one cares about other OS
print(os_type)
print(os_release)

# Determine target url based on detected OS
if os_type == "Windows" and os_release == "11":
    target_url = "https://updatefaker.com/windows11/index.html"
elif os_type == "Windows" and os_release == "10":
    target_url = "https://updatefaker.com/windows10/index.html"
elif os_type == "Windows" and os_release == "XP":
    target_url = "https://updatefaker.com/xp/index.html"
elif os_type == "Windows" or "Linux":
    target_url = "https://updatefaker.com/w98/index.html"
elif os_type == "Darwin":
    target_url = "https://updatefaker.com/osx/index.html"
else:  # Default to Windows 98 update if we don't know OS
    target_url = "https://updatefaker.com/w98/index.html"

cmd = "start chrome --user-data-dir={} --new-window --incognito --kiosk {}".format(temp_directory, target_url)
os.system(cmd)

# The Arduino we need to communicate with
arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

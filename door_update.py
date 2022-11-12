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
import random


# -------------------------------
# ----------- Classes -----------
# -------------------------------


# -------------------------------
# ---------- FUNCTIONS ----------
# -------------------------------


# -------------------------------
# ------------ Start ------------
# -------------------------------
# Override device type with arguments
# 11 = Windows 11
# 10 = Windows 10
# XP/xp = Windows XP
# 98 = Windows 98
# mac/Mac/MAC = mac
# R/r = Random

# Override flag to determine if we are overriding
override_os = False
if len(sys.argv) > 1:
    override_os = True

# temp data directory relative path
temp_dir_rel = "temp_data"
# current working directory full path
cur_dir = os.getcwd()
# Build temp directory full path for Google Chrome crap
temp_directory = "{}/{}".format(cur_dir, temp_dir_rel)
# Delete temp directory path, then recreate it
shutil.rmtree(temp_directory)
os.mkdir(temp_directory)

# Detect OS system
os_type = platform.system()  # Results can be Linux, Darwin (for mac), Windows
os_release = platform.release()  # Only useful to distinguish between Windows versions, no one cares about other OS

# Set device types to desired device if override
if override_os:
    # If we are randomizing device type, or given arg is not present...
    possible_args = ["11", "10", "XP", "xp", "98", "mac", "Mac", "MAC"]
    if sys.argv[1] not in possible_args:
        r_options = ["11", "10", "XP", "98", "mac"]
        sys.argv[1] = random.sample(r_options, 1)[0]

    # Now select device
    if sys.argv[1] == "11":
        os_type = "Windows"
        os_release = "11"
    elif sys.argv[1] == "10":
        os_type = "Windows"
        os_release = "10"
    elif sys.argv[1] == "XP" or sys.argv[1] == "xp":
        os_type = "Windows"
        os_release = "XP"
    elif sys.argv[1] == "98":
        os_type = "Windows"
        os_release = "98"
    elif sys.argv[1] == "mac" or sys.argv[1] == "Mac" or sys.argv[1] == "MAC":
        os_type = "Darwin"
        os_release = "X"  # This is irrelevant for Mac

# Determine target url based on detected OS
if os_type == "Windows" and os_release == "11":
    target_url = "https://updatefaker.com/windows11/index.html"
elif os_type == "Windows" and os_release == "10":
    target_url = "https://updatefaker.com/windows10/index.html"
elif os_type == "Windows" and os_release == "XP":
    target_url = "https://updatefaker.com/xp/index.html"
elif os_type == "Darwin":
    target_url = "https://updatefaker.com/osx/index.html"
else:  # Default to Windows 98 update if we don't know OS or if Linux
    target_url = "https://updatefaker.com/w98/index.html"

cmd = "start chrome --user-data-dir={} --new-window --incognito --kiosk {}".format(temp_directory, target_url)
os.system(cmd)

# The Arduino we need to communicate with
# arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

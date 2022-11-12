# -------------------------------
# Author: Yatish Dubasi
# Author: Tyler Spreen
# -------------------------------
import serial
import time
import pyautogui
import os
import sys
import shutil
import platform
import random


# -------------------------------
# ----------- Classes -----------
# -------------------------------
class swiper_fox:
    def __init__(self, esc_cmd, arduino_thing, random_flag, temp_directory):
        self.esc_cmd = esc_cmd
        self.arduino_thing = arduino_thing
        self.random_flag = random_flag
        self.temp_dir = temp_directory

    # Starts our "update"
    def escape_start(self):
        if not self.random_flag:
            os.system(self.esc_cmd)
        else:
            self.random_flag, self.esc_cmd = generate_escape_plan(self.temp_dir, True, "r")
            os.system(self.esc_cmd)

    # Read until we read a 0; door close
    def read_till_0(self):
        # Buffer for last few digits
        buffer = ["1", "1", "1", "1", "1"]
        data = self.arduino_thing.readline().decode('utf-8')[0]
        while buffer != ["0", "0", "0", "0", "0"]:
            data = self.arduino_thing.readline().decode('utf-8')[0]
            buffer.append(data)
            buffer = buffer[1:]
        return data

    # Read until we read a 1; door open
    def read_till_1(self):
        # Buffer for last few digits
        buffer = ["0", "0", "0", "0", "0"]
        data = self.arduino_thing.readline().decode('utf-8')[0]
        while buffer != ["1", "1", "1", "1", "1"]:
            data = self.arduino_thing.readline().decode('utf-8')[0]
            buffer.append(data)
            buffer = buffer[1:]
        return data

    # Loop that reads the comms and starts update when door open
    def looper(self):
        data = self.arduino_thing.readline().decode('utf-8')[0]
        first_round_flag = True
        while True:
            if data == "0":
                if not first_round_flag:
                    # Hold alt
                    pyautogui.keyDown("alt")
                    # Press f4
                    pyautogui.press("f4")
                    # Let go of alt
                    pyautogui.keyUp("alt")
                time.sleep(5)
                data = self.read_till_1()
                first_round_flag = False
            elif data == "1":
                self.escape_start()
                time.sleep(5)
                data = self.read_till_0()
                first_round_flag = False


# -------------------------------
# ---------- FUNCTIONS ----------
# -------------------------------
# Create escape plan
def generate_escape_plan(temp_directory_path, override_os, chosen_os=None):
    # Detect OS system
    os_type = platform.system()  # Results can be Linux, Darwin (for mac), Windows
    os_release = platform.release()  # Only useful to distinguish between Windows versions, no one cares about other OS

    # Random flag to determine if we want random OS
    random_flag = False

    # Set device types to desired device if override
    if override_os:
        # If we are randomizing device type, or given arg is not present...
        possible_args = ["11", "10", "XP", "xp", "98", "mac", "Mac", "MAC"]
        if chosen_os not in possible_args:
            random_flag = True
            r_options = ["11", "10", "XP", "98", "mac"]
            chosen_os = random.sample(r_options, 1)[0]

        # Now select device
        if chosen_os == "11":
            os_type = "Windows"
            os_release = "11"
        elif chosen_os == "10":
            os_type = "Windows"
            os_release = "10"
        elif chosen_os == "XP" or chosen_os == "xp":
            os_type = "Windows"
            os_release = "XP"
        elif chosen_os == "98":
            os_type = "Windows"
            os_release = "98"
        elif chosen_os == "mac" or chosen_os == "Mac" or chosen_os == "MAC":
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

    # Construct command to start "update"
    cmd = "start chrome --user-data-dir={} --new-window --incognito --kiosk {}".format(temp_directory_path, target_url)
    return random_flag, cmd


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

# The Arduino we need to communicate with
arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1)

if override_os:
    random_flag, cmd = generate_escape_plan(temp_directory, override_os, sys.argv[1])
else:
    random_flag, cmd = generate_escape_plan(temp_directory, override_os)

# Create our master class escape artist, Swiper the Fox
foxy = swiper_fox(cmd, arduino, random_flag, temp_directory)
foxy.looper()

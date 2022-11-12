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

# Determine target url
target_url = "https://updatefaker.com/windows11/index.html"

cmd = "start chrome --user-data-dir={} --new-window --incognito --kiosk {}".format(temp_directory, target_url)
os.system(cmd)

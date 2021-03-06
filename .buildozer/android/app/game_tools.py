"""
Copyright (c) 2015, Angello Maggio
All rights reserved.
"""

from glob import glob
from os.path import dirname, join, basename
from config import *
from kivy.app import App
import json


def best_ratio(nb, width, height):
    row = 1
    correct_ratio = 1.
    nbparrow = nb/row
    if nb % row != 0:
        nbparrow += 1
    x = float(width)/nbparrow
    y = float(height)/row
    ratio = x/y
    min_err = abs(ratio-correct_ratio)
    while ratio < correct_ratio:
        row += 1
        nbparrow = nb/row
        if nb % row != 0:
            nbparrow += 1
        x = float(width)/nbparrow
        y = float(height)/row
        ratio = x/y
        if abs(ratio-correct_ratio)> min_err:
            row -= 1
        min_err = abs(ratio-correct_ratio)
    return row


def load_data():
    sounds = {}
    icons = []
    for s in glob(join(dirname(__file__), "sounds", '*.wav')):
        name=basename(s[:-4]).split("_")[0]
        if sounds.has_key(name):
            sounds[name].append(s)
        else:
            sounds[name]=[s]
    for i in glob(join(dirname(__file__), "icons", '*.png')):
        icons.append(i)
    return sounds, icons


def load_level():
        try:
            file_name = join(App.get_running_app().user_data_dir, 'level.dat')
            with open(file_name) as fd:
                user_data = json.load(fd)
                #return user_data["items"], user_data["level"]
                return DEFAULT_NBITEMS, DEFAULT_SHOWTIME

        except IOError:
            return DEFAULT_NBITEMS, DEFAULT_SHOWTIME


def show_missing_sounds(sounds, icons):
    missing = []
    for i in icons:
        s = i.split(".png")[0].split(sep)[1]
        if s not in sounds:
            missing.append(s)
    print "missing sounds for %d players: %s" % (len(missing), missing)


def narrate(counter):
    if counter == "Goal Away":
        return "Gooooooal! For the away team!"
    elif counter == "Goal Home":
        return "Gooooooal! For the home team!"
    try:
        counter = int(counter)
    except ValueError:
        print "Wrong input."
    if counter == 1:
        return "Amazing pass forwards."
    elif counter == 2:
        return "He makes plays through the defense!"
    elif counter == 3:
        return "Alone against the goalie!!"
    elif counter == 0:
        return "They are fighting in the middle of the field."
    elif counter == -1:
        return "The enemy team makes good moves forward."
    elif counter == -2:
        return "The enemy find holes in the defense!"
    elif counter == -3:
        return "They have a chance to score!!"
    else:
        return str("Narrating error! Recieved value: " + str(counter))

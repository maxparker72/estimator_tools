import os
#GUI Imports For File Selection
import tkinter as tk
from tkinter import filedialog
from tkinter import Tk
import csv

def find_file(filename, search_path):
    for dirpath, dirnames, filenames in os.walk(search_path):
        if filename in filenames:
            return True
    return False

#Select Transmittal
application_window = tk.Tk()
pkg_original = filedialog.askdirectory(title="Please select package file:")
pkg_trans = filedialog.askopenfilename(title="Please select transmittal:")
application_window.destroy()

with open(pkg_trans, encoding = 'utf-8-sig') as checkfiles:
        reader = csv.reader(checkfiles, delimiter = ",")
        for row in reader:
            if not bool(row):
                print('skipped: {}'.format(row))
                continue
            if not (find_file(row[0], pkg_original)):
                print('{} is not in package!'.format(row[0]))


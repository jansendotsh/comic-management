#!/usr/bin/python3

import glob, os, subprocess, shutil
from sys import argv

try:
    workdir = argv[1]
    os.chdir(workdir)
except IndexError:
    workdir = os.getcwd()

for file in glob.glob("*.cbr"):
    print(file) # Just for showing the files that are in use
    print(os.path.splitext(file)[0]) # Testing for dir creation
    os.mkdir(os.path.splitext(file)[0])
    # insert for loop to identify whether os.path.isfile == True for 7z.exe, that can make this compatible with Linux & Windows
    subprocess.call(['7z', 'e', file, '-o'+os.path.splitext(file)[0]])
    subprocess.call(['7z', 'a', '-tzip', os.path.splitext(file)[0]+".cbz", os.path.splitext(file)[0]])
    shutil.rmtree(os.path.splitext(file)[0])
    os.remove(file)
    print(file+"has been successfully converted.")

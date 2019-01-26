#!/usr/bin/python3

import glob, os, subprocess, shutil, zipfile
from xml.dom import minidom
from sys import argv

try:
    workdir = argv[1]
    os.chdir(workdir)
except IndexError:
    workdir = os.getcwd()

for file in glob.glob("*.cbz"):
    metadata = zipfile.ZipFile(file, 'r')
    metaRead = metadata.read('ComicInfo.xml')
    mydoc = minidom.parseString(metaRead)

    items = mydoc.getElementsByTagName('item')
    #print(items[1].attributes['Volume'].value)
    for elem in items:  
        print(elem.firstChild.data)
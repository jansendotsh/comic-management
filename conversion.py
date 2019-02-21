#!/usr/bin/python3

import glob, os, shutil, zipfile, untangle, datetime
from sys import argv
from unrar import rarfile

try:
    workdir = os.path.abspath(argv[1])
    os.chdir(workdir)
except IndexError:
    workdir = os.getcwd()

def unpackRar(comicFile, dirPath):
    if rarfile.is_rarfile(comicFile):
        rar = rarfile.RarFile(comicFile)
        os.mkdir(dirPath)
        rar.extractall(dirPath)
    else:
        #Log error
        return

def packZip(comicFile, dirPath):
    zipped = zipfile.ZipFile(dirPath+".cbz", mode='w')

    if os.path.isdir(dirPath):
        lenDirPath = len(dirPath)
        for root, _, files in os.walk(dirPath):
            for file in files:
                filePath = os.path.join(root, file)
                zipped.write(filePath, filePath[lenDirPath :])
        zipped.close()
    else:
        #Log error here as well?
        return

for file in glob.glob("*.cbr"):
    dirPath = os.path.splitext(file)[0]

    unpackRar(file, dirPath)
    packZip(file, dirPath)

    if zipfile.is_zipfile(dirPath+".cbz"):
        shutil.rmtree(os.path.splitext(file)[0])
        os.remove(file)
    else:
        # Error on cleanup
        return
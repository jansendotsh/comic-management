#!/usr/bin/python3

import glob, os, shutil, zipfile, untangle, datetime, getopt
from sys import argv
from unrar import rarfile

helpText ='''
A script for converting CBR files to a CBZ format for openness.

Usage:

-c --convert
    Grab all CBR files in directory and convert them to CBZ format with checks

-h --help
    Print this message
        
Options:

-i --inputdir=
    The directory to search for files. If not set, will use current directory.
'''

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

def main():
    try:
        opts, args = getopt.getopt(argv[1:], "h:i:c", ["help", "inputdir=", "convert"])
    except getopt.GetoptError as err:
        print(err)
        exit()

    workDir = None
    taskConv = False

    if len(argv) == 1:
        print("No options. Run with --help for more info.")
        exit()

    for o, a in opts:
        if o in ("-h", "--help"):
            print(helpText)
            exit()
        elif o in ("-i", "--inputdir"):
            workDir = a
        elif o in ("-c", "--convert"):
            taskConv = True
        else:
            assert False, "unhandled option"

    try:
        workDir = os.path.abspath(workDir)
        os.chdir(workDir)
    except:
        workDir = os.getcwd()

    # if taskConv, indent rest
    if taskConv:
        for file in glob.glob("*.cbr"):
            dirPath = os.path.splitext(file)[0]

            unpackRar(file, dirPath)
            packZip(file, dirPath)

            # Integrity check and cleanup
            if zipfile.is_zipfile(dirPath+".cbz"):
                shutil.rmtree(os.path.splitext(file)[0])
                os.remove(file)
            else:
                # Error on cleanup
                return
        
if __name__ == '__main__':
   main() 

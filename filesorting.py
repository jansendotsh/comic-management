#!/usr/bin/python3

import glob, os, subprocess, shutil, zipfile, untangle
import datetime
from sys import argv

# Final directory for files to move
finalRoot = "/home/garrett/Comics/"

def comicParser(comicFile, finalRoot, workDir):
    zipped = zipfile.ZipFile(comicFile)

    # Extract ComicInfo.xml
    for i in zipped.namelist():
        if i.endswith("ComicInfo.xml"):
            zipped.extract(i, workDir)
    try:
        comicInfo = untangle.parse("ComicInfo.xml").ComicInfo

    except:
        print("%s does not have proper tags.\n" % (comicFile))
        comicError(comicFile, "tagErr")
        return

    # Set essential values
    comicVolume = comicInfo.Volume.cdata
    comicSeries = comicInfo.Series.cdata
    comicNumber = comicInfo.Number.cdata
    comicPublisher = comicInfo.Publisher.cdata
    comicDate = datetime.date(int(comicInfo.Year.cdata), int(comicInfo.Month.cdata), 1)

    # This is just to show that the values are working. Leaving while working on folder creation
    print("Currently sorting %s of %s, published by %s in %s, %s.\n" % (comicNumber, comicSeries, comicPublisher, comicDate.strftime('%B'), comicDate.strftime('%Y')))

    # Fixing series name conflicts
    if comicSeries is not None:
        comicSeries = comicSeries.replace(":", " -")
        comicSeries = comicSeries.replace("/", "-")
        comicSeries = comicSeries.replace("?", "")
    
    # Check variables, set empty to avoid errors while logging any missing tags
    for tag in comicVolume, comicSeries, comicNumber, comicPublisher, comicDate:
        try:
            tag
        except NameError:
            tag = None
            comicError(comicFile, "emptyValueErr")

    # Create folder
    comicPath = os.path.join(finalRoot, comicPublisher, comicSeries + " (" + comicVolume + ")")
    comicName = comicSeries + " #" + comicNumber.zfill(3) + " (" + comicDate.strftime('%B, %Y') + ").cbz"

    if not os.path.exists(comicPath):
        try:
            os.makedirs(comicPath)
        except: 
            print("An error occurred with creating %s" % (comicPath))
            return

    # Move file to newly formed folder
    if not os.path.isfile(os.path.join(comicPath, comicName)):
        shutil.move(os.path.abspath(comicFile), os.path.join(comicPath, comicName))

    # Cleaning up ComicInfo.xml work is done
    if os.path.isfile("ComicInfo.xml"):
        os.remove("ComicInfo.xml")
    
    print("File stowed.\n")

def comicError(comicFile, errType):
    currentDT = datetime.datetime.now()
    errorLogging = open("comicErr.log", "a+")

    if errType == "tagErr":
        errorLogging.write("%s - %s does not have tags, not successful.\n" % (str(currentDT), comicFile))
    
    if errType == "emptyValueErr":
        errorLogging.write("%s - %s has an empty tag field, review recommended.\n" % (str(currentDT), comicFile))

def main():
    # Grab working directory
    try:
        workdir = os.path.abspath(argv[1])
        os.chdir(workdir)
    except IndexError:
        workdir = os.getcwd()
    
    for comicFile in glob.glob("*.cbz"):
        comicParser(comicFile, finalRoot, workdir)

if __name__ == '__main__':
   main() 
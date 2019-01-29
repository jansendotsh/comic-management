#!/usr/bin/python3

import glob, os, subprocess, shutil, zipfile, untangle
import datetime
from sys import argv

finalRoot = "/home/garrett/Documents/Comics"

def comicParser(comicFile):
    try:
        comicInfo = untangle.parse("ComicInfo.xml").ComicInfo
    except:
        print("%s does not have proper tags." % (comicFile))
        # Include a print to failedTags.txt

    # Set essential values
    comicVolume = comicInfo.Volume.cdata
    comicSeries = comicInfo.Series.cdata
    comicNumber = comicInfo.Number.cdata
    comicPublisher = comicInfo.Publisher.cdata
    comicDate = datetime.date(int(comicInfo.Year.cdata), int(comicInfo.Month.cdata), 1)

    # This is just to show that the values are working. Leaving while working on folder creation
    print("Currently sorting %s of %s, published by %s in %s, %s." % (comicNumber, comicSeries, comicPublisher, comicDate.strftime('%B'), comicDate.strftime('%Y')))

    # Fixing series name conflicts
    if comicSeries is not None:
        comicSeries = comicSeries.replace(":", " -")
        comicSeries = comicSeries.replace("/", "-")
        comicSeries = comicSeries.replace("?", "")

    # Create folder
    comicPath = os.path.join(finalRoot, comicPublisher, comicSeries + " (" + comicDate.strftime('%Y') + ")")
    comicName = comicSeries + " #" + comicNumber.zfill(3) + " (" + comicDate.strftime('%B, %Y') + ").cbz"

    if not os.path.exists:
        try:
            os.makedirs(comicPath)
        except: 
            print("An error occurred with creating %s" % (comicPath))
            return

    # Move file to newly formed folder
    if not os.path.isfile(os.path.join(comicPath, comicName)):
        # This is broken... Need to test
        shutil.move(os.path.abspath(comicFile), os.path.join(comicPath, comicName))

    # Cleaning up ComicInfo.xml work is done
    os.remove("ComicInfo.xml")

def main():
    # Grab working directory
    try:
        workdir = argv[1]
        os.chdir(workdir)
    except IndexError:
        workdir = os.getcwd()

    # Final directory for files to move
    
    for comicFile in glob.glob("*.cbz"):
        zipped = zipfile.ZipFile(comicFile)

        # Extract ComicInfo.xml
        for i in zipped.namelist():
            if i.endswith("ComicInfo.xml"):
                zipped.extract(i, workdir)
        
        # Load XML file into Python
        comicParser(comicFile)

if __name__ == '__main__':
   main() 

#!/usr/bin/python3

import glob, os, subprocess, shutil, zipfile, untangle
import datetime
from sys import argv

def comicParser():
    comicInfo = untangle.parse("ComicInfo.xml").ComicInfo

    # Set essential values
    comicVolume = comicInfo.Volume.cdata
    comicSeries = comicInfo.Series.cdata
    comicNumber = comicInfo.Number.cdata
    comicPublisher = comicInfo.Publisher.cdata
    comicDate = datetime.date(int(comicInfo.Year.cdata), int(comicInfo.Month.cdata), 1)

    # This is just to show that the values are working. Leaving while working on folder creation
    print("The comic in question is nummber %s of %s and was published by %s in %s, %s." % (comicNumber, comicSeries, comicPublisher, comicDate.strftime('%B'), comicDate.strftime('%Y')))

    # Create folder

    # Move file to newly formed folder

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
    finalDirectory = "/mnt/c/Users/janseng/Documents/comicScript"

    for comicFile in glob.glob("*.cbz"):
        zipped = zipfile.ZipFile(comicFile)

        # Extract ComicInfo.xml
        for i in zipped.namelist():
            if i.endswith("ComicInfo.xml"):
                zipped.extract(i, workdir)
        
        # Load XML file into Python
        try:
            comicParser()

        except:
            print("%s does not have proper tags." % (comicFile))
            # Include a print to failedTags.txt

if __name__ == '__main__':
   main() 

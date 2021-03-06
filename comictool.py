#!/usr/bin/python3

import glob, os, shutil, zipfile, untangle, datetime, getopt
from sys import argv
from unrar import rarfile

# comictagger library tools
from comictaggerlib.options import Options
from comictaggerlib.settings import ComicTaggerSettings
from comictaggerlib.comicarchive import MetaDataStyle
from comictaggerlib import cli

helpText ='''
A script for batch managing comic books. Can convert to CBZ, automatically tag from ComicVine and sort into a folder.

Usage:

-c, --convert
    Grab all CBR files in directory and convert them to CBZ format with checks

-t, --tag
    Automatically try to grab tags from ComicVine database and save them to the file, may be interactive

-s, --sort
    Grab all tagged CBZ files in directory and move to proper stow

-h, --help
    Print this message
        
Options:

-i, --inputdir=
    The directory to search for files. If not set, will use current directory

-o, --targetdir=
    The directory to sort files int

--comicvine=
    ComicVine API key for use with online tagging
'''

class conversion:
    def unpackRar(self, comicFile, dirPath):
        if rarfile.is_rarfile(comicFile):
            rar = rarfile.RarFile(comicFile)
            os.mkdir(dirPath)
            rar.extractall(dirPath)
        else:
            comicError(comicFile, "rarErr")
            return

    def packZip(self, comicFile, dirPath):
        zipped = zipfile.ZipFile(dirPath+".cbz", mode='w')

        # Quick iteration to zip all extracted files
        if os.path.isdir(dirPath):
            lenDirPath = len(dirPath)
            for root, _, files in os.walk(dirPath):
                for file in files:
                    filePath = os.path.join(root, file)
                    zipped.write(filePath, filePath[lenDirPath :])
            zipped.close()
        else:
            #Log error here as well?
            comicError(file,"zipErr")
            return

    def __init__(self):
        for file in glob.glob("*.cbr"):
            dirPath = os.path.splitext(file)[0]

            conversion.unpackRar(self, file, dirPath)
            conversion.packZip(self, file, dirPath)

            # Integrity check and cleanup
            if zipfile.is_zipfile(dirPath+".cbz"):
                shutil.rmtree(os.path.splitext(file)[0])
                os.remove(file)
            
            else:
                # Error on cleanup
                return

            print("%s has been successfully converted.\n" % (file))

class tagging:
    ctopts = Options()
    ctsettings = ComicTaggerSettings()

    def tagger(self, comicFile, comicVineKey):
        ctopts = tagging.ctopts
        ctsettings = tagging.ctsettings

        # Setting comictagger options for cli_mode invocation
        ctopts.no_gui = True
        ctopts.save_tags = True
        ctopts.cv_api_key = comicVineKey
        ctopts.data_style = MetaDataStyle.CIX
        ctopts.search_online = True
        ctopts.verbose = True
        ctopts.parse_filename = True
        ctopts.interactive = True
        ctopts.file_list = [comicFile]
        cli.cli_mode(ctopts, ctsettings)

    def __init__(self, comicVineKey):
        ctopts = tagging.ctopts        
        ctsettings = tagging.ctsettings

        if comicVineKey is not None:
            if ctopts.cv_api_key != ctsettings.cv_api_key:
                ctsettings.cv_api_key = ctopts.cv_api_key
                ctsettings.save()
        else:
            print("No ComicVine API key provided!")
            exit()
            
        for file in glob.glob("*.cbz"):
            print(file)
            tagging.tagger(self, file, comicVineKey)

class sorting:
    def comicParser(self, comicFile, targetDir, workDir):
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
        comicPath = os.path.join(targetDir, comicPublisher, comicSeries + " (" + comicVolume + ")")
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

    def __init__(self, targetDir, workDir):
        for file in glob.glob("*.cbz"):
            sorting.comicParser(self, file, targetDir, workDir)

            print("File stowed.\n")

def comicError(comicFile, errType):
    currentDT = str(datetime.datetime.now())
    errorLogging = open("comicErr.log", "a+")

    if errType == "tagErr":
        errorLogging.write("%s - %s does not have tags, not successful\n" % (currentDT, comicFile))
    elif errType == "emptyValueErr":
        errorLogging.write("%s - %s has an empty tag field, review recommended\n" % (currentDT, comicFile))
    elif errType == "rarErr":
        errorLogging.write("%s - %s is an improper format\n" % (currentDT, comicFile))
    elif errType == "zipErr":
        errorLogging.write("%s - %s did not zip correctly, review recommended\n" % (currentDT, comicFile))
    else:
        errorLogging.write("%s - %s experienced an unhandled error, review recommended\n" % (currentDT, comicFile))

def main():
    try:
        opts, args = getopt.getopt(argv[1:], "h:io:cts", ["help", "inputdir=", "targetdir=", "comicvine=", "convert", "tag", "sort"])
    except getopt.GetoptError as err:
        print(err)
        exit()

    workDir = None
    targetDir = None
    comicVineKey = None
    taskConv = False
    taskTag = False
    taskSort = False
    
    if len(argv) == 1:
        print("No options. Run with --help for more info.")
        exit()

    for o, a in opts:
        if o in ("-h", "--help"):
            print(helpText)
            exit()
        elif o in ("-i", "--inputdir"):
            workDir = a
        elif o in ("-o", "--targetdir"):
            targetDir = a
        elif o == "--comicvine":
            comicVineKey = a
        elif o in ("-c", "--convert"):
            taskConv = True
        elif o in ("-t", "--tag"):
            taskTag = True
        elif o in ("-s", "--sort"):
            taskSort = True
        else:
            assert False, "unhandled option"

    try:
        workDir = os.path.abspath(workDir)
        os.chdir(workDir)
    except:
        workDir = os.getcwd()

    if taskConv:
        conversion()
    
    if taskTag:
        tagging(comicVineKey)
    
    if taskSort:
        # Maybe pull environ variable to alleviate consistent use? os.environ['COMICTARGET'] would work
        if targetDir is None:
            print("Unable to sort without target directory set")
            exit()

        sorting(targetDir, workDir)
                
if __name__ == '__main__':
   main() 
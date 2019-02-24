
# Comic-Management

## About

This is a repository with a series of tools that are built to help with sorting and managing digital comic book files (.cbr, .cbz). Of these tools are the following:

* **comictool.py:**
A script that unifies all functions of this pack, allowing greater automation. Currently, this script only includes converting and sorting of files. 

* **conversion.py:**
A script for converting CBR files to CBZ. *Should* work across platform yet has only been tested on Linux.

* **conversion-linux.py & conversion-win.py:**
Two small scripts for simple conversion using subprocess calls to the unrar-nonfree (on Linux or Unix-like systems) or 7-Zip (on Windows systems).

* **comictagger:**
An existing comic tagging library that interfaces with ComicVine's API and tags in an XML file. More information is available [here](https://github.com/davide-romanini/comictagger/).

* **filesorting.py:**
A script that reads ComicRack format tags from ComicTagger and sorts into appropriate folders formatted as `%Publisher%/%series% (%volume%)/%series% %number (%month%, %year%)` An example of this is `Black Hammer #001.cbz` being moved and renamed to `Dark Horse Comics/Black Hammer (2016)/Black Hammer #001 (July, 2016).cbz` The formatting of sorting is hard coded although can be changed.

## Requirements

* Python 3
* For agonstic conversion: libunrar or [UnRARDLL.exe](http://www.rarlab.com/rar/UnRARDLL.exe), more info [here](https://www.rarlab.com/rar_add.htm)
* For OS-specific conversion: unrar-free (Linux/Unix-like) or 7-Zip (Windows)
* virtualenv

## Preparation

* Clone repository
* `cd comic-management`
* `virtualenv .`
* `source bin/activate`
* `python3 -m pip install -r requirements.txt`

If using without virtualenv, you may experience issues although can work normally.

## Usage

* **comictool.py:**
Based on what you want to use the tool for, you can choose the arguments. Help text is printing below:

```markdown
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
```

Examples of usage would be as follows:
```bash
# For converting files:
./comictool.py -c -i /home/source/unsorted-comics

# For tagging: 
./comictool.py -t /home/source/unsorted-comics

# For sorting and stowing files:
./comictool.py -s -i /home/source/unsorted-comics -o /home/source/Documents/Comics
```

* **conversion.py (will be removed)**
Simply run the command as listed below. Directory argument is optional. If not passed, script will use current working directory.

```bash
./conversion.py -c --inputdir=<Directory>
```

* **conversion-linux.py or conversion-win.py (will be removed):**

Both scripts will be used similarly with the following command:

```bash
./conversion-linux.py <Directory>
```

If left empty, will begin working on converting all files in the current directory.

**WARNING:** If you do not have the right version of unrar, you risk deleting all of your files. Best to create a backup of your first folder and test prior to using widely. Since unrar-free and unrar-nonfree use the same command, there isn't a way to differentiate the two programmatically. If you have a solution, feel feel to pull request to help.

* **comictagger:**

To use ComicTagger to tag files with the correctly formatted tags in the right format, the below command will work:

```bash
comictagger --cv-api-key <ComicVine API Key> -s -t cr -o -v -f -i '*.cbz'
```

A ComicVine API key can be obtained [here](https://comicvine.gamespot.com/api/).

Additional features and usage can be found in ComicTagger's [Wiki](https://github.com/davide-romanini/comictagger/wiki/UserGuide#cli-user-guide).

* **filesorting.py (will be removed)**

To sort files, you can use a similarly formatted request to the conversion script:

```bash
./filesorting.py <Directory>
```

As with the conversion script, this will use current directory if none given. Additionally, in any working directory, a comicErr.log file will be generated if there are any errors to be reported from the files passed through the directory.

## Credits

* ComicTagger and the Python 3 rewrite by David Romanini.

# Comic-Management

## About

This is a repository with a series of tools that are built to help with sorting and managing digital comic book files (.cbr, .cbz). Of these tools are the following:

* **conversion-linux.py:**
A small script that converts CBR files to CBZ on Linux and Unix-like systems using unrar-free.

* **conversion-win.py:**
A similar small script that converts CBR files to CBZ on Windows systems using the 7-Zip executable.

* **comictagger:**
An existing comic tagging library that interfaces with ComicVine's API and tags in an XML file. More information is available [here](https://github.com/davide-romanini/comictagger/).

* **filesorting.py:**
A script that reads ComicRack format tags from ComicTagger and sorts into appropriate folders formatted as `%Publisher%/%series% (%volume%)/%series% %number (%month%, %year%)` An example of this is `Black Hammer #001.cbz` being moved and renamed to `Dark Horse Comics/Black Hammer (2016)/Black Hammer #001 (July, 2016).cbz` The formatting of sorting is hard coded although can be changed.

## Requirements

* Python 3
* unrar-free (Linux/Unix-like) or 7-Zip (Windows)
* virtualenv

## Preparation

* Clone repository
* cd comic-management
* virtualenv .
* source bin/activate
* python3 -m pip install -r requirements.txt

Is able to be used without virtualenv although you will need to assess the versions of libraries used.

## Usage

* **conversion-linux.py or conversion-win.py:**

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

* **filesorting.py**

To sort files, you can use a similarly formatted request to the conversion script:

```bash
./filesorting.py <Directory>
```

As with the conversion script, this will use current directory if none given. Additionally, in any working directory, a comicErr.log file will be generated if there are any errors to be reported from the files passed through the directory.

## Credits

* ComicTagger and the Python 3 rewrite by David Romanini.
#!/usr/bin/python3
"""
Moves comic files based on metadata organizing in a tree by Publisher/Series (Volume)
"""

"""
This script is based on make_links.py by Anthony Beville

Copyright 2015  Fabio Cancedda, Anthony Beville

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import os
import platform
import shutil

from comictaggerlib.comicarchive import *
from comictaggerlib.settings import *
from comictaggerlib.issuestring import *
import comictaggerlib.utils

def make_folder( folder ):
   if not os.path.exists( folder ):
      try:
         os.makedirs(folder)
      except Exception as e:
         print("{0} Can't make {1} -- quitting".format(e, folder))
         quit()
         
def move_file( source, filename ):
   if not os.path.exists( filename ):
      shutil.move( os.path.abspath(source) , filename )

def main():
   utils.fix_output_encoding()
   settings = ComicTaggerSettings()

   style = MetaDataStyle.CIX

   if platform.system() == "Windows":
      print("Sorry, this script works only on UNIX systems", file=sys.stderr)
      
   if len(sys.argv) < 3:
      print("usage:  {0} comic_root tree_root".format(sys.argv[0]), file=sys.stderr)
      return
   
   comic_root = sys.argv[1]
   tree_root = sys.argv[2]
   
   print("Root is : ", comic_root)
   if not os.path.exists( comic_root ):
      print("The comic root doesn't seem a directory or it doesn't exists. -- quitting", file=sys.stderr)
      return
   
   filelist = utils.get_recursive_filelist( [ comic_root ] )
      
   if len(filelist) == 0:
      print("The comic root seems empty. -- quitting", file=sys.stderr)
      return
      
   make_folder( tree_root )
      
   #first find all comics with metadata
   print("Reading in all comics...")
   comic_list = []
   max_name_len = 2
   for filename in filelist:
      ca = ComicArchive(filename, settings.rar_exe_path )
      if ca.seemsToBeAComicArchive() and ca.hasMetadata( style ):

         comic_list.append((filename, ca.readMetadata( style )))
         
         max_name_len = max ( max_name_len, len(filename))
         fmt_str = "{{0:{0}}}".format(max_name_len)
         print(fmt_str.format( filename ) + "\r", end=' ', file=sys.stderr)
         sys.stderr.flush()

   print(fmt_str.format( "" ), file=sys.stderr)

   print("Found {0} tagged comics.".format( len(comic_list)))

   # walk through the comic list and moves each one   
   for filename, md in comic_list:
      print(fmt_str.format( filename ) + "\r", end=' ', file=sys.stderr)
      sys.stderr.flush()
      
      #do publisher/series organizing:
      fixed_series_name = md.series
      if fixed_series_name is not None:
         # some tweaks to keep various filesystems happy
         fixed_series_name = fixed_series_name.replace(":", " -")
         fixed_series_name = fixed_series_name.replace("/", "-")
         fixed_series_name = fixed_series_name.replace("?", "")
      series_folder = os.path.join(tree_root, str(md.publisher), str(fixed_series_name) + " (" + str(md.volume) + ")")
      make_folder( series_folder )
      move_file( filename, os.path.join(series_folder, os.path.basename(filename)) )
      
if __name__ == '__main__':
   main() 

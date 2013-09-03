#!/usr/bin/env python

import argparse
import sys
from sys import stdout
import os
import hashlib
from timeleft import timeleft

parser = argparse.ArgumentParser(description='find determines if the "from" files are duplicated in the "to" files')
parser.add_argument('fromAndTo', nargs='*', default=[],
                    help='directories/files to recurse and use as from and to arguments')
parser.add_argument('--from', default=[], nargs='*',
                    help='the files from recursing that are determined to be duplicates (ie: the ones that are reported)')
parser.add_argument('--to', default=[], nargs='*',
                    help='the files from recursing that are determined to be duplicated (ie: the ones that are not reported)')
parser.add_argument('--out',
                    help=
"""the file to write the duplicate files with format
<md5>\t<from file that is duplicating>\t<to-file1 that was duplicated>\t...\t<to-filen>
""")
args = vars(parser.parse_args())
parser.parse_args(sys.argv[1:len(sys.argv)])

fromPaths = args['from']
toPaths = args['to']
for bothPath in args['fromAndTo']:
  fromPaths.append(bothPath)
  toPaths.append(bothPath)

if len(fromPaths) == 0:
  parser.print_help()
  sys.exit("no from files/dir provided")
if len(toPaths) == 0:
  parser.print_help()
  sys.exit("no to files/dir provided")

outputFile = open(args['out'], 'w')


def getPath(folder, file):
  if folder.endswith("/") :
    return folder + file
  else:
    return folder + "/" + file

# if the file does not exist, return an empty string
def computeMd5(filePath):
  try:
    with open(filePath, 'rb') as fh:
      m = hashlib.md5()
      while True:
        data = fh.read(8192)
        if not data:
          break
        m.update(data)
      return m.hexdigest()
  except IOError:
    return ""

fromFiles = []
toFiles = []

print "fromPaths = " + " ".join(fromPaths)
print "toPaths = " + " ".join(toPaths)

print "recursively finding all to files"
for dir in toPaths:
  for folder, subs, fs in os.walk(dir):
    for file in fs:
      toFiles.append( getPath(folder , file ) )
print "we have " + str(len(toFiles)) + " to files"

print "recursively finding all from files"
for dir in fromPaths:
  for folder, subs, fs in os.walk(dir):
    for file in fs:
      fromFiles.append( getPath(folder , file ) )
print "we have " + str(len(fromFiles)) + " from files"

status = timeleft( len(fromFiles) + len(toFiles) )

hashes = dict()
for file in toFiles:
  md5 = computeMd5(file)
  dupeFiles = hashes.get(md5)
  if dupeFiles == None:
    dupeFiles = []
    hashes[md5] = dupeFiles
  dupeFiles.append(file)
  status.complete_unit()
  stdout.write("\r" + status.pretty_string() + "               ")
  stdout.flush()
  

for file in fromFiles:
  md5 = computeMd5(file)
  dupeFiles = hashes.get(md5)
  if dupeFiles != None:
    outputFile.write(md5 + "\t" + file + "\t" + "\t".join(dupeFiles) + "\n")
  status.complete_unit()
  # the long string of space characters is to clear the previous line
  # just in case the new line is shorter. When testing this, I noticed
  # that characters from the previously written line would now be cleared
  # when using \r only replaced by the next line.
  stdout.write("\r" + status.pretty_string() + "               ")
  stdout.flush()

print ""
outputFile.close()
print "done"
  

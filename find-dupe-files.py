#!/usr/bin/env python

import sys
import os

import hashlib

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

files = []

# we store all files so that we can
# say how many are left to process
#   an alternative is to iterate over the
#   files and keep a count
#   and walk the files a second time
print "recursively finding all files"
for dir in sys.argv:
  for folder, subs, fs in os.walk(dir):
    for file in fs:
      files.append( getPath(folder , file ) )
print "found " + str(len(files)) + " files."

filesDone = 0

# mapping of a file's hash to all the files that have that hash
# all files with the empty hash are files that could
# not be processed
hashes = dict()
print "finding duplicates"
for file in files:
  md5 = computeMd5(file)
  dupeFiles = hashes.get(md5, [])
  dupeFiles.append(file)


  filesDone = filesDone + 1
  print str(float(filesDone) / float(len(files)) * 100) + "% done ( " + str(filesDone) + " out of " + str(len(files)) + " ) "
  

print "printing dupes"
for key, value in hashes.iteritems():
  if len(value) > 1 :
    print key + value.join("\t")

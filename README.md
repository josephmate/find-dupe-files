find-dupe-files
===============

Well, this is embarrassing. There is a unix tool that already does this:
fdupes. Move along, nothing to see here.

=========================================================

NOTE: both option does not work. (only --from --to works)

NOTE: i removed the timing estimate stuff for now!


Finds duplicate files in the list of directories you provide

motivation:
I was trying to use fslint and there was no progress indicator. I put together this
script to give a better indication of progress than fslint.

usage:
./find-dupe-files.py  dir1 dir2 dir3 ... dirn

example:
./find-dupe-files.py  /home/jmate/blah

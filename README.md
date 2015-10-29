Musicsort
=============
Please note that this is **not** a finished and complete program, but rather a quick and dirty script to do a very specific task I needed.

Requirements
---------------
`musicsort.py` depends on `mutagen` for ID3 handling and `click` for the command line interface.

Compability
----------
Anyways, Musicsort works with Python3 only (If you add `__future__` imports it may work with python2, too) and depends on `mutagen` for ID3 tag handling.'

What it actually does
--------------
Suppose you have a bunch of mp3 files in one directory that are not structured in any way (but do have ID3 tags). What the script does, is sort these mp3 files into directories grouped by artist and album.
So the file:
`Song - Album - Artist.mp3` gets moved to `./artist/album/` (regardless of the filename though, it uses the ID3 tags)

Usage
-----------
Install the necessary dependencies by running `pip install -r requirements.txt`. Then just do:
```
python3 musicsort.py ~/Music/foldertosort
```
be sure to point it to the actual folder where your music to be sorted is located.

Development
------------
As I didn't find any software that would do this for me quickly I wrote this script. It uses click for CLI stuff and is pretty extensible. Pull requests are welcome. Unit tests are nowhere near being finished by the way.

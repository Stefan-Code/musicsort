#!/usr/bin/python3
"""
This module allows to quickly sort mp3 files lying around into subfolders based on ID3 tags.
That means the files are sorted into folders
based on the Artist and Album. (To be customizable in the future)
If your mp3s don't have ID3 tags on them, fix it using e.g. picard or MP3Tag.
"""
from mutagen.mp3 import EasyMP3
import os
import glob
import click
import string
import shutil
from click import echo

class MP3:
    """
    Represents a mp3 file
    """
    def __init__(self, path):
        self.path = path
        if os.path.isfile(path):
            self._mutagen_mp3 = EasyMP3(path)
        else:
            raise FileNotFoundError("File {} not found".format(path))
    @property
    def artist(self):
        """
        Returns the artist name of the mp3.
        If the artist isn't set in the tags, return "" (an empty string)
        """
        return self._mutagen_mp3["artist"][0] or ""

    @property
    def title(self):
        """
        Returns the title of the mp3.
        If the title isn't set in the tags, return "" (an empty string)
        """
        return self._mutagen_mp3["title"][0] or ""

    @property
    def album(self):
        """
        Returns the album name of the mp3.
        If the album isn't set in the tags, return "" (an empty string)
        """
        return self._mutagen_mp3["album"][0] or ""

@click.command()
@click.argument('directory', required=True)
@click.option('--dry-run', is_flag=True)
def cli(directory, dry_run):
    """
    Main function called by click
    """
    echo("Looking for mp3s in" + directory)
    mp3s = get_mp3_paths(directory)
    echo("found {} mp3s".format(len(mp3s)))
    if dry_run:
        echo("dry run - not moving any files")
    for mp3_path in mp3s:
        try:
            mp3 = MP3(mp3_path)
            oldpath = mp3_path
            root = os.path.dirname(oldpath)
            filename = os.path.basename(oldpath)
            newpath = os.path.join(root, "{}/{}/".format(make_filesystem_safe(mp3.artist),
                                                         make_filesystem_safe(mp3.album)))
            newfilepath = os.path.join(newpath, filename)
            echo("{} -> {}".format(oldpath, newpath))
            # actual moving:
            if not dry_run:
                mkdir_recursive(newpath)  # make sure the dir we're moving to exists
                shutil.move(oldpath, newfilepath)
            # echo("{} {} {}".format(mp3.artist, mp3.album, mp3.title))
        except Exception as e:  # pylint: disable=W0703
            echo("Having trouble with {} : {}".format(mp3_path, e))
            raise

def get_mp3_paths(path):
    """
    Returns the relative paths of all *.mp3 files in a given directory (path)
    """
    if not os.path.isdir(path):
        raise FileNotFoundError("The Directory you specified does not exist")
    paths = []

    for filename in glob.iglob(os.path.join(path, '*.mp3')):
        paths.append(os.path.join(filename))
    return paths

def make_filesystem_safe(filename):
    """
    Accepts a filename as argument and returns the file system safe version of it.
    Do not pass a complete path like ~/directory/file.name here!
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in filename if c in valid_chars)

def mkdir_recursive(path):
    """
    Checks if path is an existing directory.
    If not, recursively creates all directories for path to exist.
    """
    sub_path = os.path.dirname(path)
    if not os.path.exists(sub_path):
        mkdir_recursive(sub_path)
    if not os.path.exists(path):
        os.mkdir(path)

if __name__ == "__main__":
    cli()

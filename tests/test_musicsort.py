"""
Module for testing the musicsort module
"""
import pytest
import sys
import os
import random
import shutil
sys.path.append(os.path.abspath("."))
from musicsort import MP3
import musicsort

class TestMP3():
    def setup(self):
        self.mp3 = MP3("tests/test.mp3")
    def testArtist(self):
        assert self.mp3.artist == "Artist Test Value"
    def testAlbum(self):
        assert self.mp3.album == "Album Test Value"
    def testTitle(self):
        assert self.mp3.title == "Title Test Value"

@pytest.fixture(scope="module")
def mp3files(request):
    def make_mp3s():
        os.mkdir("tests/mp3s/")
        os.mkdir("tests/mp3s/sub/")
        touch("tests/mp3s/1.mp3")
        touch("tests/mp3s/2.mp3")
        touch("tests/mp3s/3.mp3")
        touch("tests/mp3s/sub/1.mp3")
        touch("tests/mp3s/sub/2.mp3")
    def fin():
        try:
            shutil.rmtree("tests/mp3s/")
            pass
        except FileNotFoundError:
            pass
        except:
            print("--- Removing MP3 test directory failed! ---")
            raise
    request.addfinalizer(fin)
    try:
        make_mp3s()
    except FileExistsError:
        print("--- tests directory dirty! ---")
        #cleanup
        fin()
        #retry
        make_mp3s()


class TestMP3Finder:
    def testGetMp3s(self, mp3files):
        results = musicsort.get_mp3_paths("tests/mp3s/")
        mp3s = ["tests/mp3s/1.mp3",
                "tests/mp3s/2.mp3",
                #"tests/mp3s/sub/1.mp3",
                #"tests/mp3s/sub/2.mp3",
                ]
        for mp3 in mp3s:
            assert mp3 in results
        assert("tests/mp3s/2.mp")

def test_make_filesystem_safe():
    pairs = [("Hello World", "Hello World"),
             ("some thing else", "some thing else"),
             ("Hello/World", "HelloWorld"),
             ("Hello&*()$# World", "Hello() World")]
    for pair in pairs:
        assert musicsort.make_filesystem_safe(pair[0]) == pair[1]

def test_mkdir_recursive():
    directory1 = "./tests/"+random_alpha(10)+"/"
    directory2 = directory1 + random_alpha(5)+"/"
    try:
        musicsort.mkdir_recursive(directory2)
        assert os.path.isdir(directory2)
    finally:
        os.rmdir(directory2)
        os.rmdir(directory1)
        assert not os.path.isdir(directory2)
        assert not os.path.isdir(directory1)

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

def random_alpha(length):
    return ''.join(random.choice('0123456789ABCDEF') for i in range(length))

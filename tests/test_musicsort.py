import pytest
import sys
import os
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

def test_make_filesystem_safe():
    pairs = [("Hello World", "Hello World"),
             ("some thing else", "some thing else"),
             ("Hello/World", "HelloWorld"),
             ("Hello&*()$# World", "Hello() World")]
    for pair in pairs:
        assert musicsort.make_filesystem_safe(pair[0]) == pair[1]

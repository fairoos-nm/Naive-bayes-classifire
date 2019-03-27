#test_classifier

import classifier
import os

def test_current_working_dir():
    assert classifier.current_working_dir() == "/home/fairoos/lycaeum_projects/song_lyrics_classifier"

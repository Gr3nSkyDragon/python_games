"""Find game files whether running from source or as a built exe.

build.cmd lays the games out like this:

    Games/
        resources/              shared images and sounds
        Scuba Reader/
            Scuba Reader.exe
            scuba_words.txt     editable word list

When running a .py file from the repo, resources/ sits next to the script and
editable text files are read from their folder inside resources/.
"""
import os
import sys

FROZEN = getattr(sys, 'frozen', False)

if FROZEN:
    GAME_DIR = os.path.dirname(sys.executable)
    RESOURCES_DIR = os.path.join(os.path.dirname(GAME_DIR), 'resources')
else:
    GAME_DIR = os.path.dirname(os.path.abspath(__file__))
    RESOURCES_DIR = os.path.join(GAME_DIR, 'resources')


def resource(*parts):
    """Path to a shared image or sound, e.g. resource('icon', 'star.jpg')."""
    return os.path.join(RESOURCES_DIR, *parts)


def editable(folder, filename):
    """Path to an editable text file: next to the exe when built, resources/<folder>/ otherwise."""
    if FROZEN:
        return os.path.join(GAME_DIR, filename)
    return resource(folder, filename)


def local(filename):
    """Path to a file the game writes, such as a save file: next to the exe, or the repo root."""
    return os.path.join(GAME_DIR, filename)

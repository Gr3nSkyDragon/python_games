"""Convert PNG icons to .ico so build.cmd can embed them in the exes.

usage: python tools/icon_converter.py resources/icon/wheel.png [more.png ...]
Writes wheel.ico next to each PNG.
"""
import os
import sys

from PIL import Image

if len(sys.argv) < 2:
    sys.exit(__doc__)

for png in sys.argv[1:]:
    ico = os.path.splitext(png)[0] + '.ico'
    Image.open(png).save(ico, format='ICO')
    print(f"{png} -> {ico}")

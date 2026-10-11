"""Shrink oversized images in resources/ to roughly the size the games show them.

Before an image is shrunk, its full-size original is copied to originals/ at the
same path (e.g. originals/star/families/-un/bun.png). originals/ is not in git;
zip it for releases. To restore full size, copy originals/ over resources/.

Running it again only touches images that are still over their limit, such as
newly added ones.

usage: python tools/shrink_images.py [--dry-run]
"""
import os
import shutil
import sys

from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES = os.path.join(REPO, 'resources')
ORIGINALS = os.path.join(REPO, 'originals')

DEFAULT_LIMIT = 1024


def limit_for(rel_path):
    """Longest side, in pixels, an image needs at the size its game draws it."""
    if rel_path.startswith('background/') or 'background' in os.path.basename(rel_path):
        return 1920  # drawn to fill the whole window
    if rel_path.startswith('red_alphabet/'):
        return 1440  # Letter Reveal draws letters at full window height
    return DEFAULT_LIMIT


def shrink(path, limit):
    img = Image.open(path)
    img.load()
    if img.mode == 'P':
        # palette images can only be resized pixelated; convert for smooth resizing
        img = img.convert('RGBA')
    img.thumbnail((limit, limit), Image.LANCZOS)
    if path.lower().endswith('.png'):
        img.save(path, 'PNG', optimize=True)
    else:
        img.convert('RGB').save(path, 'JPEG', quality=90)


def main():
    dry_run = '--dry-run' in sys.argv
    before = after = count = 0
    for folder, _, files in os.walk(RESOURCES):
        for name in sorted(files):
            if not name.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
            path = os.path.join(folder, name)
            rel = os.path.relpath(path, RESOURCES).replace(os.sep, '/')
            limit = limit_for(rel)
            with Image.open(path) as img:
                size = img.size
            if max(size) <= limit:
                continue
            count += 1
            old_bytes = os.path.getsize(path)
            before += old_bytes
            if dry_run:
                print(f"would shrink {rel} {size[0]}x{size[1]} -> max {limit}px")
                continue
            original = os.path.join(ORIGINALS, *rel.split('/'))
            os.makedirs(os.path.dirname(original), exist_ok=True)
            shutil.copy2(path, original)
            shrink(path, limit)
            after += os.path.getsize(path)
            print(f"{rel}: {size[0]}x{size[1]} {old_bytes / 1e6:.1f} MB -> {os.path.getsize(path) / 1e6:.2f} MB")
    if dry_run:
        print(f"{count} images over their limit ({before / 1e6:.1f} MB)")
    else:
        print(f"Shrunk {count} images: {before / 1e6:.1f} MB -> {after / 1e6:.1f} MB. Originals are in {ORIGINALS}")


if __name__ == '__main__':
    main()

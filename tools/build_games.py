"""Build the games into Games/, rebuilding only the ones that changed. Run it through build.cmd.

    build.cmd                   rebuild games that changed since their last build
    build.cmd "Star CVC" ...    rebuild just these games, changed or not
    build.cmd --all             wipe Games/ and rebuild everything (use this for releases)

A game counts as changed when its exe is missing or anything built into the exe differs from
its last build: its script, the repo's own modules it imports (paths.py, speech.py, ...), its
icon, or the Python and library versions. Fingerprints of those are kept in build/stamps/.

Shared resources and the Game Guide are synced every run (only changed files are copied).
Editable text files are copied next to an exe only when missing, so edits made in Games/
survive a rebuild; --all starts them fresh from resources/.
"""
import ast
import hashlib
import importlib.metadata
import os
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMES_DIR = os.path.join(REPO, 'Games')
BUILD_DIR = os.path.join(REPO, 'build')
STAMPS_DIR = os.path.join(BUILD_DIR, 'stamps')

# script, exe name, icon (in resources/icon), editable text files (in resources/)
GAMES = [
    ('alphabet_blast.py',    'Alphabet Blast',    'apple.ico',         []),
    ('alphabet_galaxy.py',   'Alphabet Galaxy',   'telescope.ico',     []),
    ('cowboy.py',            'Cowboy',            'cowboy_hat.ico',    ['cowboy/cowboy.txt']),
    ('cvc_slots.py',         'CVC Slots',         'slots.ico',         ['slots/slot_letters.txt']),
    ('find_the_princess.py', 'Find the Princess', 'princess_icon.ico', ['princess/hidden_content.txt',
                                                                        'princess/rectangle_content.txt']),
    ('letter_pop.py',        'Letter Pop',        'balloon.ico',       ['letter_pop/poppers.txt']),
    ('letter_reveal.py',     'Letter Reveal',     'reveal.ico',        ['reveal/letters.txt']),
    ('phonicsmon.py',        'Phonicsmon',        'phonics.ico',       []),
    ('random_wheel_spin.py', 'Random Wheel Spin', 'wheel.ico',         []),
    ('scuba_reader.py',      'Scuba Reader',      'snorkel.ico',       ['scuba/scuba_words.txt']),
    ('star_cvc.py',          'Star CVC',          'star.ico',          []),
    ('word_maker.py',        'Word Maker',        'robot.ico',         []),
]

# Installed libraries whose version is baked into every exe
LIBRARIES = ['pygame', 'comtypes', 'pyinstaller']


def local_modules(script, found=None):
    """The repo's own .py modules a script imports, directly or through each other."""
    found = set() if found is None else found
    with open(os.path.join(REPO, script), encoding='utf-8') as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names = [node.module]
        else:
            continue
        for name in names:
            module = name.split('.')[0] + '.py'
            if module not in found and os.path.isfile(os.path.join(REPO, module)):
                found.add(module)
                local_modules(module, found)
    return found


def fingerprint(script, icon):
    """A hash of everything that goes into the game's exe."""
    digest = hashlib.sha256()
    files = [script] + sorted(local_modules(script)) + [os.path.join('resources', 'icon', icon)]
    for path in files:
        digest.update(path.encode() + b'\0')
        with open(os.path.join(REPO, path), 'rb') as f:
            digest.update(f.read())
    digest.update(sys.version.encode())
    for library in LIBRARIES:
        digest.update(f"{library}={importlib.metadata.version(library)}".encode())
    return digest.hexdigest()


def stamp_path(name):
    return os.path.join(STAMPS_DIR, name + '.txt')


def is_up_to_date(name, script, icon):
    exe = os.path.join(GAMES_DIR, name, name + '.exe')
    try:
        with open(stamp_path(name)) as f:
            return os.path.isfile(exe) and f.read().strip() == fingerprint(script, icon)
    except OSError:
        return False


def build(name, script, icon):
    print(f"Building {name}...", flush=True)
    result = subprocess.run([
        sys.executable, '-m', 'PyInstaller', '--noconfirm', '--log-level', 'WARN', '--onefile', '--windowed',
        '--name', name, '--icon', os.path.join(REPO, 'resources', 'icon', icon),
        '--distpath', os.path.join(GAMES_DIR, name), '--workpath', BUILD_DIR, '--specpath', BUILD_DIR,
        os.path.join(REPO, script)], cwd=REPO)
    if result.returncode != 0:
        sys.exit(f"Building {name} failed.")
    os.makedirs(STAMPS_DIR, exist_ok=True)
    with open(stamp_path(name), 'w') as f:
        f.write(fingerprint(script, icon))


def copy_text_files(name, text_files):
    """Editable text files go next to the exe; existing copies (maybe edited) are kept."""
    for text_file in text_files:
        target = os.path.join(GAMES_DIR, name, os.path.basename(text_file))
        if not os.path.exists(target):
            shutil.copy2(os.path.join(REPO, 'resources', *text_file.split('/')), target)


def sync_shared_files():
    # /MIR copies only changed files and removes ones deleted from resources/.
    # Text files go next to each exe instead, so they're left out here.
    result = subprocess.run(['robocopy', os.path.join(REPO, 'resources'), os.path.join(GAMES_DIR, 'resources'),
                             '/MIR', '/XF', '*.txt', '*.py', '/NFL', '/NDL', '/NJH', '/NJS', '/NP'],
                            stdout=subprocess.DEVNULL)
    if result.returncode >= 8:  # robocopy: below 8 means success
        sys.exit("Copying resources failed.")
    shutil.copy2(os.path.join(REPO, 'Game Guide.docx'), GAMES_DIR)


def main(args):
    names = [game[1] for game in GAMES]
    rebuild_all = '--all' in args
    requested = [a for a in args if a != '--all']
    unknown = [a for a in requested if a.lower() not in (n.lower() for n in names)]
    if unknown:
        sys.exit(f"No game named {', '.join(unknown)}. Games: {', '.join(names)}")

    if rebuild_all and os.path.isdir(GAMES_DIR):
        shutil.rmtree(GAMES_DIR)
    os.makedirs(GAMES_DIR, exist_ok=True)

    built, current = [], []
    for script, name, icon, text_files in GAMES:
        if requested:
            needed = name.lower() in (r.lower() for r in requested)
        else:
            needed = rebuild_all or not is_up_to_date(name, script, icon)
        if needed:
            build(name, script, icon)
            built.append(name)
        else:
            current.append(name)
        if os.path.isdir(os.path.join(GAMES_DIR, name)):
            copy_text_files(name, text_files)

    print("Syncing shared resources...", flush=True)
    sync_shared_files()
    print()
    print(f"Rebuilt: {', '.join(built) if built else 'nothing - every game was up to date'}")
    if current and not requested:
        print(f"Already up to date: {', '.join(current)}")
    print(f"Games are in {GAMES_DIR}")


if __name__ == '__main__':
    main(sys.argv[1:])

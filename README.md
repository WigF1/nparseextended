# nParseExtended for Project1999

Extended version of nParse with more functional custom triggers. Provides player location and spell tracking support for Project 1999 by reading the player log.

----

Running from source
========

Setup:

1. Create the directory where you would like nParse to be cloned to and then `cd` into the directory.
2. Clone the repository: `git clone https://github.com/WigF1/nparseextended.git .`  
3. Create a virtual environment: `python -m venv .venv`
4. Activate the virtual environment: 
    - Windows: `.\.venv\Scripts\activate.bat`
    - Linux: `source .venv/bin/activate`
5. Install pip requirements: `pip install -r requirements.txt`

Usage:

1. Activate the virtual environment: 
    - Windows: `.\.venv\Scripts\activate.bat`
    - Linux: `source .venv/bin/activate`
2. Run nParse from the repository directory: `python nparse.py`

nParse reads `data/` and writes `nparse.config.json` relative to the directory it is started from, so always start it from the repository directory.

----

Development
========

Follow the "Running from source" setup above, then run nParse with `python nparse.py`.

`test/fake_loc_sender.py` sends fake player locations to a location server, which is useful for testing location sharing on the map.

----

Building
========

Setup:

1. Complete the "Running from source" setup above.
2. Install PyInstaller: `pip install pyinstaller`
3. Linux only: the splash screen needs tkinter at build time. Install your distribution's Tk package for Python, e.g. `sudo dnf install python3-tkinter` (Fedora) or `sudo apt install python3-tk` (Debian/Ubuntu).

Usage:

1. Build nParse: `pyinstaller --clean nparse_py.spec`
2. The compiled nParse executable will be in:
    - Windows: `dist\nparse.exe`
    - Linux: `dist/nparse`

The executable bundles Python, the libraries, fonts and UI files, but not the map and spell data. Those are read from a `data/` folder next to where nParse is started, so a release must ship them alongside the executable:

```
nparse-<version>/
├── nparse            (nparse.exe on Windows)
└── data/
    ├── maps/
    └── spells/
```

Do not include `nparse.config.json`, `data/voices/` or `data/sounds/`; these hold your own settings, downloaded voice models and trigger sounds, and are created on first use.

Packaging a Linux release:

```bash
VER=1.0.0
mkdir -p release/nparse-$VER/data
cp dist/nparse release/nparse-$VER/
cp -r data/maps data/spells release/nparse-$VER/data/
tar -C release -czf nparse-$VER-linux-x86_64.tar.gz nparse-$VER
```

Linux builds only run on distributions whose glibc is the same version or newer than the one on the build machine. To support older distributions, build on an older distribution (for example in a container).

Before publishing, extract the archive into an empty directory, `cd` into it, run `./nparse`, and check that maps load, spell timers appear and "Test Voice" in the settings speaks.

Publishing a GitHub release:

```bash
git tag v$VER && git push origin v$VER
gh release create v$VER nparse-$VER-linux-x86_64.tar.gz --title "v$VER" --notes "..."
```

----

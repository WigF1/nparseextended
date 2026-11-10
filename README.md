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
2. Run nParse from the repository directory: `python nparseextended.py`

nParse reads `data/` and writes `nparse.config.json` relative to the directory it is started from, so always start it from the repository directory.

----

Development
========

Follow the "Running from source" setup above, then run nParse with `python nparseextended.py`.

`test/fake_loc_sender.py` sends fake player locations to a location server, which is useful for testing location sharing on the map.

----

Building
========

Setup:

1. Complete the "Running from source" setup above.
2. Install PyInstaller: `pip install pyinstaller`
3. Linux only: the splash screen needs tkinter at build time. Install your distribution's Tk package for Python, e.g. `sudo dnf install python3-tkinter` (Fedora) or `sudo apt install python3-tk` (Debian/Ubuntu).
4. Windows only: replace PyQt5's bundled Visual C++ runtime DLLs (see below). Repeat this whenever the virtual environment is recreated or PyQt5 is reinstalled.

Windows: replacing PyQt5's Visual C++ runtime

PyQt5 ships an old copy of the Visual C++ runtime (`msvcp140.dll` 14.26) in `PyQt5\Qt5\bin`. onnxruntime, used by piper-tts for voice output, needs 14.40 or newer and crashes if PyQt5's copy is loaded first. The build then fails with `Isolated subprocess crashed while importing package 'onnxruntime'`, and a built executable would crash as soon as voice output loads.

To check, run `python -c "import PyQt5.QtCore, onnxruntime; print('ok')"`. If it exits without printing `ok`, replace PyQt5's runtime DLLs with the newer copies from System32 (the original files are kept as `.bak`):

```powershell
$qt = ".venv\Lib\site-packages\PyQt5\Qt5\bin"
Get-ChildItem "$qt\*140*.dll" | ForEach-Object {
    $sys = "C:\Windows\System32\$($_.Name)"
    if (Test-Path $sys) {
        Copy-Item $_.FullName "$($_.FullName).bak" -Force
        Copy-Item $sys $_.FullName -Force
        "{0}: {1}" -f $_.Name, (Get-Item $_.FullName).VersionInfo.FileVersion
    }
}
```

Each replaced file should report version 14.40 or higher. If System32's copies are older than that, install the latest [Microsoft Visual C++ Redistributable (x64)](https://aka.ms/vs/17/release/vc_redist.x64.exe) on the build machine first.

This is only needed on the build machine. PyInstaller bundles these DLLs into `nparse-extended.exe`, so users do not need to install the Visual C++ Redistributable. To confirm a build works without it, run it in Windows Sandbox, which starts from a clean copy of Windows.

Usage:

1. Set the release version in `CURRENT_VERSION` near the top of `nparseextended.py`, e.g. `major=0, minor=2, patch=0` for release `v0.2.0`, and commit it. The update check compares this against the latest GitHub release, so a build with an old version number tells its users to update to the version they already have.
2. Build nParse: `pyinstaller --clean nparse_py.spec`
3. The compiled nParse executable will be in:
    - Windows: `dist\nparse-extended.exe`
    - Linux: `dist/nparse-extended`

The executable bundles Python, the libraries, fonts and UI files, but not the map and spell data. Those are read from a `data/` folder next to where nParse is started, so a release must ship them alongside the executable:

```
nParseExtended/
├── nparse-extended   (nparse-extended.exe on Windows)
└── data/
    ├── maps/
    └── spells/
```

Do not include `nparse.config.json`, `data/voices/` or `data/sounds/`; these hold your own settings, downloaded voice models and trigger sounds, and are created on first use.

The folder inside the archive is always called `nParseExtended` (the version is only in the archive's file name), so users can upgrade by extracting a new release over their existing folder. Their settings, trigger sounds and voice models are kept because the archive does not contain them.

Packaging a Linux release:

```bash
VER=1.0.0
rm -rf release && mkdir -p release/nParseExtended/data
cp dist/nparse-extended release/nParseExtended/
cp -r data/maps data/spells release/nParseExtended/data/
tar -C release -czf nparse-$VER-linux-x86_64.tar.gz nParseExtended
```

Linux builds only run on distributions whose glibc is the same version or newer than the one on the build machine. To support older distributions, build on an older distribution (for example in a container).

Packaging a Windows release (PowerShell):

```powershell
$VER = "1.0.0"
$dir = "release\nParseExtended"
Remove-Item -Recurse -Force release -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force "$dir\data" | Out-Null
Copy-Item dist\nparse-extended.exe $dir
Copy-Item -Recurse data\maps, data\spells "$dir\data"
Compress-Archive -Path $dir -DestinationPath "nparse-$VER-windows-x64.zip" -Force
```

Windows builds run on Windows 10 and 11. If UPX is installed on the build machine, PyInstaller compresses the bundled DLLs with it, which can break the Qt and onnxruntime DLLs and trigger antivirus false positives; either uninstall UPX or set `upx=False` in `nparse_py.spec`. The executable is not code-signed, so Windows SmartScreen shows an "unknown publisher" warning the first time it is run ("More info", then "Run anyway").

Before publishing, extract the release into an empty directory and start nParse from there (`./nparse-extended` on Linux, double-click `nparse-extended.exe` on Windows). Check that the splash screen appears, maps load, spell timers appear, a trigger sound plays and "Test Voice" in the settings speaks. The first voice test downloads the voice model, so it needs an internet connection.

Publishing a GitHub release (from either machine, using the same `VER`):

Release notes come from `CHANGELOG.md`. Add changes under "Unreleased" as you work, and before releasing rename that heading to `## v<version> - <date>` and add a new empty "Unreleased" heading above it. Each version's section should say what is new, changed and fixed, how to upgrade, and how to install. The "Check for Updates" setting sends users to the latest release page, so the upgrade steps in the notes are what they will follow.

```bash
git tag v$VER && git push origin v$VER
# extract this version's section of CHANGELOG.md into the notes file
awk -v h="## v$VER " 'index($0, h) == 1 {f=1; next} /^## / {f=0} f' CHANGELOG.md > release-notes.md
gh release create v$VER --title "v$VER" --notes-file release-notes.md
gh release upload v$VER nparse-$VER-linux-x86_64.tar.gz    # from the Linux build machine
gh release upload v$VER nparse-$VER-windows-x64.zip        # from the Windows build machine
```

Tag and create the release once, then upload each platform's archive from the machine that built it.

----

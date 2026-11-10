# Changelog

## Unreleased

## v0.2.0 - 2026-11-10

Numerous fixes and a new nomenclature for the app and folder

### New

- **Charm timers clear when charm breaks.** When "Your charm spell has worn off." appears, timers for charm spells such as Call of Karana, Allure of the Wild and Thrall of Bones are removed.

### Fixed

- Spells that share their name with an NPC or item spell now get timers again, for example Savage Spirit, Acumen, Enduring Breath, Selo's Song of Travel, Steelskin and Ultravision. nParse was using the NPC version's cast time and messages, so it never saw these spells land.
- Spells whose duration depends only on your level now get timers, for example Glamour of Tunare, Malise, Malisement, Feckless Might, Insipid Weakness, Gaze, Magnify and Bind Sight. They were previously given a 0-second timer that vanished immediately.
- An interrupted spell no longer gets a timer if its landing message appears later, for example from someone else casting the same spell.
- Trigger voice and sound alerts now play while the Spells window is hidden. Spell and trigger timers also keep running in the background, so they are up to date when the window is shown again.
- "Check for Updates" works again. It now checks this project's GitHub releases, and the "Update Available" item in the tray menu opens the latest release page. Previously it checked a server that no longer exists and linked to the original nParse project.

### Changed

- The program is now called `nparse-extended` (`nparse-extended.exe` on Windows) and comes in a folder called `nParseExtended`. The folder name no longer includes the version, so future updates can be extracted straight over it.

### Upgrading from v0.1.0

This version's folder has a new name, so settings need to be copied over once:

1. Extract this release next to your existing `nparse-0.1.0` folder. It creates a folder called `nParseExtended`.
2. Copy these from `nparse-0.1.0` into `nParseExtended`, if you have them:
   - `nparse.config.json`: your settings and custom triggers.
   - `data/sounds/`: the sound files your triggers play. Without it, sound alerts are silent.
   - `data/voices/`: downloaded voice models. Without it, they download again the first time voice is used.
3. Run `nparse-extended` (`nparse-extended.exe` on Windows) from the `nParseExtended` folder. Once everything works, you can delete `nparse-0.1.0`.

From the next release on, upgrading is simpler: extract the new release into the folder that contains `nParseExtended` and let it replace the existing files. Your settings, trigger sounds and voice models are kept. On Windows, "Extract All" suggests a new folder named after the zip file; change it to the folder that contains `nParseExtended`.

### Install

- **Windows:** download `nparse-<version>-windows-x64.zip`, extract it, and run `nparse-extended.exe` from the `nParseExtended` folder. Windows may show an "unknown publisher" warning the first time; choose "More info", then "Run anyway".
- **Linux:** download `nparse-<version>-linux-x86_64.tar.gz`, extract it, `cd nParseExtended` and run `./nparse-extended`. Requires a recent distribution (glibc 2.43 or newer, e.g. Fedora 44).
- Always start nParseExtended from inside its folder, because it reads its map and spell data from there.

## v0.1.0 - 2026-11-10

First release of nParseExtended, an extended version of nParse for Project 1999.

### New

- **Trigger categories.** Each custom trigger has a category, and its name is set automatically to "Category - Trigger text". Triggers in the same category are grouped together in the Spells window.
- **Named groups in triggers.** With "Use Regex" on, named groups such as `(?P<target>\w+)` can be used in the trigger name and spoken text as `{target}`.
- **Voice alerts.** Triggers can speak when they match, when their timer is about to end, and when it ends. Speech uses a natural-sounding voice (Male or Female) that runs on your computer, with an adjustable speaking rate. Turn it on under Settings → Voice.
- **Sound alerts.** Triggers can play a WAV or MP3 file when they match. Volume and on/off are under Settings → Sound.
- **Alert-only triggers.** Leave a trigger's time blank to have it speak or play a sound without creating a timer.
- **Plane of Mischief map.** Added static maze mobs, roamer indicators and roaming paths, with confirmed locations.

### Changed

- Levitate now lasts 12 minutes, consistent with Pegasus Feather Cloak.
- New icon, logo and splash screen.

### Fixed

- Triggers that allow duplicates no longer reuse an existing timer when an earlier one expires; each match adds its own timer.
- Voice output no longer hangs on Linux when the audio device stops responding.

### Upgrading from nParse

- Keep your existing `nparse.config.json`. Your settings and custom triggers are kept, and existing triggers are placed in the "Custom" category.
- Once this version saves your settings, older versions of nParse can no longer read that config file. Back it up first if you might go back.

### Install

- **Windows:** download `nparse-0.1.0-windows-x64.zip`, extract it, and run `nparse.exe` from the extracted folder. Windows may show an "unknown publisher" warning the first time; choose "More info", then "Run anyway".
- **Linux:** download `nparse-0.1.0-linux-x86_64.tar.gz`, extract it, `cd` into the folder and run `./nparse`. Requires a recent distribution (glibc 2.43 or newer, e.g. Fedora 44).
- Always start nParse from inside its folder, because it reads its map and spell data from there.
- The first time a voice is used, its model (about 60 MB) is downloaded, so an internet connection is needed once.

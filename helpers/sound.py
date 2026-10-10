"""
Cross-platform sound file playback (WAV and MP3), backed by Qt's QMediaPlayer.

QMediaPlayer hands decoding and output to the platform's own media stack
(Windows Media Foundation, macOS AVFoundation, GStreamer on Linux), so MP3
support depends on the user having the usual codecs installed. Playback is
asynchronous and must happen on the Qt main thread, which is where parsers
run, so play() is safe to call straight from Parser.parse().

Sounds chosen in the trigger settings are copied into data/sounds/ and
referenced by filename only, so configs don't break when moved between
machines or operating systems.
"""
import filecmp
import os
import shutil

from PyQt5.QtCore import QUrl

from helpers import config

try:
    from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
except ImportError:  # QtMultimedia missing from this PyQt5 build; sound output just no-ops
    QMediaContent = None
    QMediaPlayer = None

SOUND_DIR = os.path.join('data', 'sounds')
FILE_FILTER = 'Sound files (*.wav *.mp3)'
_DEFAULT_VOLUME = 100

_players = {}  # absolute path : QMediaPlayer (kept alive, or Qt stops playback)


def is_available():
    """Returns True if QtMultimedia is available."""
    return QMediaPlayer is not None


def play(filename):
    """Plays a sound from data/sounds/, honoring the global sound settings."""
    sound_settings = config.data.get('sound', {})
    if not sound_settings.get('enabled', True):
        return
    _play(filename, sound_settings.get('volume', _DEFAULT_VOLUME))


def play_preview(filename, volume=None):
    """Plays a sound immediately, ignoring sound:enabled. Used by 'Test' buttons."""
    if volume is None:
        volume = config.data.get('sound', {}).get('volume', _DEFAULT_VOLUME)
    _play(filename, volume)


def resolve_path(filename):
    """Returns the absolute path of a sound stored in data/sounds/."""
    return os.path.abspath(os.path.join(SOUND_DIR, filename))


def import_sound(source_path):
    """Copies a user-chosen sound file into data/sounds/ and returns its filename.

    Re-importing the same file reuses the existing copy; a different file with
    the same name gets a numeric suffix rather than overwriting it.
    """
    os.makedirs(SOUND_DIR, exist_ok=True)
    source_path = os.path.abspath(source_path)
    if os.path.dirname(source_path) == os.path.abspath(SOUND_DIR):
        return os.path.basename(source_path)

    base, ext = os.path.splitext(os.path.basename(source_path))
    filename = base + ext
    index = 2
    while os.path.exists(resolve_path(filename)):
        if filecmp.cmp(source_path, resolve_path(filename), shallow=False):
            return filename
        filename = '{}_{}{}'.format(base, index, ext)
        index += 1
    shutil.copy2(source_path, resolve_path(filename))
    return filename


def _play(filename, volume):
    if not filename or not is_available():
        return
    path = resolve_path(filename)
    if not os.path.exists(path):
        return
    player = _players.get(path)
    if player is None:
        player = QMediaPlayer()
        player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        _players[path] = player
    player.setVolume(volume)
    player.stop()  # restart from the beginning if it's already playing
    player.play()

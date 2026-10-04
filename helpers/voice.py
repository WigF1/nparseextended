"""
Cross-platform text-to-speech, backed by Piper (local neural TTS).

Piper (https://github.com/OHF-Voice/piper1-gpl) runs small offline neural
voice models via onnxruntime. It sounds dramatically more natural than the
OS-level formant synthesizers pyttsx3 falls back to (espeak/espeak-ng in
particular, which is what's available on Linux), while still being fully
local: no internet or API key needed for actual speech, no per-utterance
network round trip. A voice's model files (~60MB) are fetched once and
cached under data/voices/ the first time that voice is used.

Each call to speak() renders audio on a background thread (onnxruntime
inference and the eventual WAV playback both take real time) and plays it
through a plain platform media command, so speech never blocks the Qt UI.
"""
import os
import platform
import subprocess
import tempfile
import threading
import wave
from pathlib import Path

from helpers import config

try:
    from piper.voice import PiperVoice
    from piper.config import SynthesisConfig
    from piper.download_voices import download_voice
except ImportError:  # piper-tts is an optional dependency; voice output just no-ops without it
    PiperVoice = None
    SynthesisConfig = None
    download_voice = None

# Medium-quality voices, explicitly named/documented by their creators as
# male/female (unlike e.g. 'amy', which turns out to be a fine-tune of
# 'lessac's own weights and ends up sounding much like it - these two are
# unrelated models and reliably distinct).
_VOICE_MODELS = {
    'male': 'en_US-hfc_male-medium',
    'female': 'en_US-hfc_female-medium',
}
_DEFAULT_GENDER = 'male'

_VOICE_DIR = os.path.join('data', 'voices')
_DEFAULT_RATE = 175  # matches the settings window's baseline rate slider value

_voice_cache = {}  # model name : PiperVoice
_cache_lock = threading.Lock()
_warned_models = set()  # avoids repeating the same download-failure message


def is_available():
    """Returns True if piper-tts is installed."""
    return PiperVoice is not None


def speak(text):
    """Speaks `text` asynchronously, honoring the global voice:enabled setting."""
    if not text or not is_available():
        return
    voice_settings = config.data.get('voice', {})
    if not voice_settings.get('enabled', False):
        return
    _speak_async(
        text,
        voice_settings.get('gender', 'default'),
        voice_settings.get('rate', _DEFAULT_RATE)
    )


def speak_preview(text, gender='default', rate=_DEFAULT_RATE):
    """Speaks `text` immediately with explicit settings, ignoring voice:enabled.

    Used by the settings window's 'Test Voice' button to preview options
    before they're saved. If the chosen voice hasn't been used before, this
    is also what triggers its one-time model download.
    """
    if not text or not is_available():
        return
    _speak_async(text, gender, rate)


def _speak_async(text, gender, rate):
    thread = threading.Thread(
        target=_speak_sync, args=(text, gender, rate), daemon=True)
    thread.start()


def _model_name_for_gender(gender):
    return _VOICE_MODELS.get(gender, _VOICE_MODELS[_DEFAULT_GENDER])


def _get_voice(model_name):
    """Loads (and caches) a PiperVoice, downloading its model files on first use."""
    with _cache_lock:
        voice = _voice_cache.get(model_name)
        if voice is not None:
            return voice

        os.makedirs(_VOICE_DIR, exist_ok=True)
        model_path = os.path.join(_VOICE_DIR, '{}.onnx'.format(model_name))
        if not os.path.exists(model_path):
            try:
                download_voice(model_name, Path(_VOICE_DIR))  # one-time fetch, needs internet
            except Exception:
                if model_name not in _warned_models:
                    _warned_models.add(model_name)
                    print(
                        "nParse voice: couldn't download the '{}' voice model "
                        "(needs internet the first time it's used).".format(model_name)
                    )
                return None

        voice = PiperVoice.load(model_path)
        _voice_cache[model_name] = voice
        return voice


def _speak_sync(text, gender, rate):
    try:
        voice = _get_voice(_model_name_for_gender(gender))
        if voice is None:
            return
        # Piper has no literal "words per minute" - length_scale is a
        # phoneme-duration multiplier (<1 faster, >1 slower), so approximate
        # the old rate slider by scaling around its default value.
        syn_config = SynthesisConfig(length_scale=_DEFAULT_RATE / max(rate, 1))

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            wav_path = tmp.name
        try:
            with wave.open(wav_path, 'wb') as wav_file:
                voice.synthesize_wav(text, wav_file, syn_config=syn_config)
            _play_wav(wav_path)
        finally:
            try:
                os.remove(wav_path)
            except OSError:
                pass
    except Exception:
        # Voice output is a convenience feature; a broken/missing TTS
        # dependency should never surface as an error in the main parser.
        pass


def _play_wav(path):
    system = platform.system()
    if system == 'Darwin':
        subprocess.run(['afplay', path], check=False)
    elif system == 'Windows':
        import winsound  # noqa: PLC0415 (Windows-only stdlib module)
        winsound.PlaySound(path, winsound.SND_FILENAME)
    else:
        subprocess.run(['aplay', '-q', path], check=False)

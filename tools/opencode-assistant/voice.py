import asyncio
import ctypes
import os
import struct
import math
import tempfile
import wave

import edge_tts

EDGE_VOICE = "zh-TW-HsiaoChenNeural"
SAPI_VOICE_NAME = "han"


def _play_mp3(path: str) -> None:
    mci = ctypes.windll.winmm.mciSendStringW
    mci(f'open "{path}" alias tts_play', None, 0, 0)
    mci("play tts_play wait", None, 0, 0)
    mci("close tts_play", None, 0, 0)


async def speak(text: str) -> None:
    try:
        communicate = edge_tts.Communicate(text, voice=EDGE_VOICE)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_path = tmp.name
        await communicate.save(tmp_path)
        _play_mp3(tmp_path)
        os.unlink(tmp_path)
    except Exception:
        _speak_sapi(text)


def _speak_sapi(text: str) -> None:
    try:
        import win32com.client
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        for v in speaker.GetVoices():
            if SAPI_VOICE_NAME in v.Id.lower():
                speaker.Voice = v
                break
        speaker.Rate = 0
        speaker.Volume = 100
        speaker.Speak(text, 1)
    except Exception:
        print(f"  🤖 {text}", flush=True)


def play_wake_sound() -> None:
    sr = 44100
    duration = 0.15
    freq = 880
    frames = int(sr * duration)
    data = b"".join(
        struct.pack("<h", int(0.3 * 32767 * math.sin(2 * math.pi * freq * i / sr)))
        for i in range(frames)
    )
    path = os.path.join(tempfile.gettempdir(), "_xiaoting_beep.wav")
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(data)
    mci = ctypes.windll.winmm.mciSendStringW
    mci(f'open "{path}" alias beep_play', None, 0, 0)
    mci("play beep_play wait", None, 0, 0)
    mci("close beep_play", None, 0, 0)

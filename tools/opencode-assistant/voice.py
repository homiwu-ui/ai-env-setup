import asyncio
import ctypes
import io
import os
import tempfile
import wave

import edge_tts
import numpy as np
import sounddevice as sd
import speech_recognition as sr

EDGE_VOICE = "zh-TW-HsiaoChenNeural"
SAPI_VOICE_NAME = "han"

_sample_rate = 16000
_channels = 1
_dtype = np.int16


def _save_wav_bytes(audio_data: np.ndarray) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(_channels)
        wf.setsampwidth(2)
        wf.setframerate(_sample_rate)
        wf.writeframes(audio_data.tobytes())
    return buf.getvalue()


_quiet = False

def listen(timeout: float = 5.0, phrase_limit: float = 8.0) -> str | None:
    if not _quiet:
        print("🎤 聆聽中...（說「結束」離開）", flush=True)
    recorded = sd.rec(
        int(_sample_rate * phrase_limit),
        samplerate=_sample_rate,
        channels=_channels,
        dtype=_dtype,
        blocking=True,
    )
    wav_bytes = _save_wav_bytes(recorded)
    recognizer = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(wav_bytes)) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="zh-TW")
        if not _quiet:
            print(f"  你說：{text}", flush=True)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        if not _quiet:
            print("  ⚠️ Google 語音辨識連線失敗，請檢查網路", flush=True)
        return None


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
        if not _quiet:
            print(f"  🤖 {text}", flush=True)


def play_wake_sound() -> None:
    import struct, math
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

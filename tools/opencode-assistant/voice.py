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


def listen(timeout: float = 5.0, phrase_limit: float = 8.0) -> str | None:
    print("🎤 聆聽中..." + "（說「結束」離開）" if not None else "", flush=True)
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
        print(f"  你說：{text}", flush=True)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        print("  ⚠️ Google 語音辨識連線失敗，請檢查網路", flush=True)
        return None


def _play_mp3(path: str) -> None:
    mci = ctypes.windll.winmm.mciSendStringW
    alias = "tts_playback"
    cmd_open = f'open "{path}" alias {alias}'
    cmd_play = f"play {alias} wait"
    cmd_close = f"close {alias}"
    mci(cmd_open, None, 0, 0)
    mci(cmd_play, None, 0, 0)
    mci(cmd_close, None, 0, 0)


def speak(text: str) -> None:
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        communicate = edge_tts.Communicate(text, voice=EDGE_VOICE)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp_path = tmp.name
        loop.run_until_complete(communicate.save(tmp_path))
        loop.close()
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
    duration = 0.15
    t = np.linspace(0, duration, int(44100 * duration), False)
    tone = 0.3 * np.sin(2 * np.pi * 880 * t)
    sd.play(tone, samplerate=44100)
    sd.wait()

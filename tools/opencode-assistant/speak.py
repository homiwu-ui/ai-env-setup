import sys
import win32com.client

SAPI_VOICE_PRIORITY = ["hsiaochen", "hanhan"]


def speak(text: str) -> None:
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    chosen = None
    for priority in SAPI_VOICE_PRIORITY:
        for v in speaker.GetVoices():
            vid = v.Id.lower()
            if priority in vid:
                chosen = v
                if "native" in vid:
                    break
        if chosen:
            break
    if chosen:
        speaker.Voice = chosen
    speaker.Rate = 0
    speaker.Volume = 100
    speaker.Speak(text, 0)


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if text:
        speak(text)

import sys
import win32com.client

SAPI_VOICE = "han"


def speak(text: str) -> None:
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    for v in speaker.GetVoices():
        if SAPI_VOICE in v.Id.lower():
            speaker.Voice = v
            break
    speaker.Rate = 0
    speaker.Volume = 100
    speaker.Speak(text, 1)


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    if text:
        speak(text)

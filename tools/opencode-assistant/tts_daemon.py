import os
import time
import win32com.client

QUEUE = os.path.join(os.path.dirname(__file__), "_speak_queue.txt")
SAPI_VOICE = "han"

speaker = win32com.client.Dispatch("SAPI.SpVoice")
for v in speaker.GetVoices():
    if SAPI_VOICE in v.Id.lower():
        speaker.Voice = v
        break
speaker.Rate = 0
speaker.Volume = 100

last_size = 0
if os.path.exists(QUEUE):
    last_size = os.path.getsize(QUEUE)

while True:
    if os.path.exists(QUEUE):
        size = os.path.getsize(QUEUE)
        if size > last_size:
            with open(QUEUE, "r", encoding="utf-8") as f:
                f.seek(last_size)
                for line in f:
                    text = line.strip()
                    if text:
                        speaker.Speak(text, 1)
            last_size = size
    time.sleep(0.05)

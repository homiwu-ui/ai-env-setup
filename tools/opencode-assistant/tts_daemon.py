import os
import time
import win32com.client

QUEUE = os.path.join(os.path.dirname(__file__), "_speak_queue.txt")

speaker = win32com.client.Dispatch("SAPI.SpVoice")
for priority in ["hsiaochen", "hanhan"]:
    found = None
    for v in speaker.GetVoices():
        vid = v.Id.lower()
        if priority in vid:
            found = v
            if "native" in vid:
                break
    if found:
        speaker.Voice = found
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
                        speaker.Speak(text, 0)
            last_size = size
    time.sleep(0.05)

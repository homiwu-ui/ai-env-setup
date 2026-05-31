import os
import sys

QUEUE = os.path.join(os.path.dirname(__file__), "_speak_queue.txt")
text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
if text:
    with open(QUEUE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

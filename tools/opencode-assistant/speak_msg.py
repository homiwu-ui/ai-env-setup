import os
import sys

BASE = r"G:\我的雲端硬碟\AI 專項\tools\opencode-assistant"
sys.path.insert(0, BASE)
from chat import respond

QUEUE = os.path.join(BASE, "_speak_queue.txt")


def _speak(text: str) -> None:
    try:
        with open(QUEUE, "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except Exception:
        import speak as s
        s.speak(text)


def main():
    args = sys.argv[1:]
    raw = False
    if "--raw" in args:
        raw = True
        args.remove("--raw")
    text = " ".join(args) if args else "hi"
    if raw:
        reply = text
    else:
        reply = respond(text)
    if reply == "EXIT":
        _speak("哼！那我先走啦～有事再叫我！Bye bye！")
        print("EXIT")
        return
    _speak(reply)
    print(reply)


if __name__ == "__main__":
    main()

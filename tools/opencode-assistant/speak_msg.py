import sys

sys.path.insert(0, r"G:\我的雲端硬碟\AI 專項\tools\opencode-assistant")
import speak
from chat import respond


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
        speak.speak("哼！那我先走啦～有事再叫我！Bye bye！")
        print("EXIT")
        return
    speak.speak(reply)
    print(reply)


if __name__ == "__main__":
    main()

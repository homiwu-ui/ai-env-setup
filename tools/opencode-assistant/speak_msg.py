import asyncio
import sys

sys.path.insert(0, r"G:\我的雲端硬碟\AI 專項\tools\opencode-assistant")
import voice
from chat import respond


async def main():
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
        await voice.speak("哼！那我先走啦～有事再叫我！Bye bye！")
        print("EXIT")
        return
    await voice.speak(reply)
    print(reply)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import sys

sys.path.insert(0, r"G:\我的雲端硬碟\AI 專項\tools\opencode-assistant")
from chat import respond


def _speak_edge(text: str) -> None:
    import edge_tts, tempfile, os, ctypes

    async def _run():
        c = edge_tts.Communicate(text, voice="zh-TW-HsiaoChenNeural")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            path = tmp.name
        await c.save(path)
        mci = ctypes.windll.winmm.mciSendStringW
        mci(f'open "{path}" alias sp', None, 0, 0)
        mci("play sp wait", None, 0, 0)
        mci("close sp", None, 0, 0)
        os.unlink(path)

    asyncio.run(_run())


def _speak_sapi(text: str) -> None:
    import win32com.client
    s = win32com.client.Dispatch("SAPI.SpVoice")
    for v in s.GetVoices():
        if "han" in v.Id.lower():
            s.Voice = v
            break
    s.Rate = 0
    s.Volume = 100
    s.Speak(text, 1)


def _speak(text: str) -> None:
    try:
        _speak_edge(text)
    except Exception:
        _speak_sapi(text)


def main():
    args = sys.argv[1:]
    raw = False
    quick = False
    if "--raw" in args:
        raw = True
        args.remove("--raw")
    if "--quick" in args:
        quick = True
        args.remove("--quick")
    text = " ".join(args) if args else "hi"
    if raw:
        reply = text
    else:
        reply = respond(text)
    if reply == "EXIT":
        _speak("哼！那我先走啦～有事再叫我！Bye bye！")
        print("EXIT")
        return
    if quick:
        _speak_sapi(reply)
    else:
        _speak(reply)
    print(reply)


if __name__ == "__main__":
    main()

import time
import asyncio
import edge_tts
import tempfile
import os
import ctypes

t0 = time.time()

async def main():
    text = "你好帥哥庭，我是小婷，今天想問什麼？"
    c = edge_tts.Communicate(text, voice="zh-TW-HsiaoChenNeural")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        path = tmp.name
    await c.save(path)
    t1 = time.time()
    mci = ctypes.windll.winmm.mciSendStringW
    mci(f'open "{path}" alias p', None, 0, 0)
    mci("play p wait", None, 0, 0)
    mci("close p", None, 0, 0)
    os.unlink(path)
    t2 = time.time()
    print(f"TTS生成: {t1-t0:.2f}s, 播放: {t2-t1:.2f}s, 總計: {t2-t0:.2f}s")

asyncio.run(main())

import asyncio
import sys

import voice
import history
from chat import respond


async def voice_loop() -> None:
    voice.play_wake_sound()
    await voice.speak(respond("hi"))
    while True:
        user_text = voice.listen()
        if user_text is None:
            continue
        reply = respond(user_text)
        if reply == "EXIT":
            await voice.speak("哼！那我先走啦～有事再叫我！Bye bye！")
            break
        await voice.speak(reply)
        history.save_turn(user_text, reply)


async def text_loop() -> None:
    print("小婷：", end="", flush=True)
    voice.play_wake_sound()
    greeting = respond("hi")
    await voice.speak(greeting)
    print(greeting, flush=True)
    while True:
        try:
            user_text = input("你：").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user_text:
            continue
        reply = respond(user_text)
        if reply == "EXIT":
            await voice.speak("哼！那我先走啦～有事再叫我！Bye bye！")
            print("小婷：哼！那我先走啦～有事再叫我！Bye bye！", flush=True)
            break
        await voice.speak(reply)
        print(f"小婷：{reply}", flush=True)
        history.save_turn(user_text, reply)


def main() -> None:
    if "--hidden" in sys.argv:
        voice._quiet = True
        asyncio.run(voice_loop())
    elif "--text" in sys.argv:
        asyncio.run(text_loop())
    else:
        asyncio.run(voice_loop())


if __name__ == "__main__":
    main()

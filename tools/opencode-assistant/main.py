import asyncio
import sys

import voice
import history
from chat import respond


async def main_loop() -> None:
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
            print("小婷：有事再叫我喔，掰掰～", flush=True)
            break
        await voice.speak(reply)
        print(f"小婷：{reply}", flush=True)
        history.save_turn(user_text, reply)


def main() -> None:
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\n👋 小婷已關閉", flush=True)


if __name__ == "__main__":
    main()

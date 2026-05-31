import asyncio
import signal
import sys

import voice
import history
from chat import respond


async def main_loop() -> None:
    voice.play_wake_sound()
    greeting = respond("hi")
    await voice.speak(greeting)

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


def main() -> None:
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("\n👋 助手已關閉", flush=True)


if __name__ == "__main__":
    main()

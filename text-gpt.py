#!/usr/bin/env python3
import os
import sys
import time
import threading
import itertools
from openai import OpenAI

def spinner_task(stop_event):
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if stop_event.is_set():
            break
        sys.stdout.write(f'\r{c}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 20 + '\r')
    sys.stdout.flush()

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Defina a variável OPENAI_API_KEY.")
        exit(1)

    client = OpenAI(api_key=api_key)

    history = [
        {
            "role": "system",
            "content": (
                "You are a virtual assistant that can search the web. You are running in a Linux terminal. "
                "Always return plain text only, without Markdown formatting. The output should be suitable for direct display in a Linux terminal."
            )
        }
    ]

    while True:
        try:
            user_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nSaindo.")
            break

        history.append({"role": "user", "content": user_input})

        # inicia spinner em thread separada
        stop_event = threading.Event()
        spinner = threading.Thread(target=spinner_task, args=(stop_event,), daemon=True)
        spinner.start()

        # chamada à Responses API
        resp = client.responses.create(
            model="gpt-4.1-mini",
            input=history,
            tools=[
                {"type": "web_search_preview"}
            ]
        )

        # para o spinner
        stop_event.set()
        spinner.join()

        answer = resp.output_text.strip()
        print(f"\n\033[0;32m{answer}\033[0m\n")

        history.append({"role": "assistant", "content": answer})
        if len(history) > 20:
            history = history[-20:]

if __name__ == "__main__":
    main()
